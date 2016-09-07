import sublime, sublime_plugin
from subprocess import Popen

import os

try:  # python 3
    from .functions import surroundingTeXEquation, makeOutput, readPreamble, ENVIRON
except ValueError:  # python 2
    from functions import surroundingTeXEquation, makeOutput, readPreamble, ENVIRON


isRun = False
resFileName = None
runProc = None

def makeFile(view):
    sel = view.sel()[0]
    
    code = surroundingTeXEquation(
            view.substr(sublime.Region(0, view.size())),
            sel.begin()
        )

    if not code:
        return None

    settings = sublime.load_settings("TeXPreview.sublime-settings")    

    always_load_preamble = settings.get("always_load_preamble")
    load_preamble_after_error = settings.get("load_preamble_after_error") 

    if (always_load_preamble == True):
        preamble = readPreamble(view.substr(sublime.Region(0, view.size())))
    else:
        preamble = None

    nResFileName = makeOutput(code, preamble, os.path.dirname(view.file_name()))

    if (load_preamble_after_error == True):
        if (nResFileName == None):
            preamble = readPreamble(view.substr(sublime.Region(0, view.size())))
            nResFileName = makeOutput(code, preamble,os.path.dirname(view.file_name()))

    return nResFileName


def applicationReload(view):
    global isRun
    global resFileName
    global runProc


    nResFileName = makeFile(view)
    if (nResFileName == None):
        return

    if (runProc != None):        
        if (runProc.poll() == None):
            runProc.kill()

    if (resFileName != None):
        while ((os.path.exists(resFileName))):
            try:
                os.unlink(resFileName)
            except Exception:
                pass
    resFileName = nResFileName
   
    try:
        pdf_open_app = sublime.load_settings("TeXPreview.sublime-settings").get("pdf_open_app")
        runProc = Popen((pdf_open_app + " " + str(resFileName)).split(), env=ENVIRON)
        
    except Exception as e:
        sublime.error_message('LaTeX Preview: Could not open the file! '+ str(resFileName))
        raise e

    isRun = True

def changePic(view):
    
    global resFileName

    nResFileName = makeFile(view)

    if (nResFileName == None):
        return 
    try:
        os.remove(resFileName)
        os.rename(nResFileName, resFileName)

    except Exception as e:
        os.remove(nResFileName)
        sublime.error_message('LaTeX Preview: Could not change the file! ' +  str(resFileName))
        raise e


class LatexPreviewEvent(sublime_plugin.EventListener):
    
    def on_selection_modified_async(self, view):
        
        global isRun
        global resFileName
        global runProc
        
        if ((runProc != None) and (runProc.poll() != None)):
            runProc = None
            isRun = False
            if ((os.path.exists(resFileName))):
                os.unlink(resFileName)
            return

        if (isRun == False):
            return

        auto_reload = sublime.load_settings("TeXPreview.sublime-settings").get("auto_reload") 
        
        if (auto_reload == False):
            return
        if (auto_reload == "application_reload"):
            applicationReload(view)
            return

        changePic(view)
        

    def on_load_async(self, view):
        ENVIRON['PATH'] += sublime.load_settings("TeXPreview.sublime-settings").get("latex_path")

        

    def on_pre_close(self, view):
        global isRun
        global resFileName
        if (isRun == True):
            os.unlink(resFileName)
        dirPath = os.path.dirname(view.file_name())+os.path.sep +r'TeX_Preview_tmp'

        if ((os.path.exists(dirPath))):
            os.rmdir(dirPath)


class LatexPreviewCommand(sublime_plugin.TextCommand):

    def run(self, view):
        applicationReload(self.view)


class LatexStopPreviewCommand(sublime_plugin.TextCommand):
    def run(self, view):

        global isRun
        global resFileName
        global runProc

        isRun = False
        if (runProc != None):        
            if (runProc.poll() == None):
                runProc.kill()

        if (resFileName != None):
            while ((os.path.exists(resFileName))):
                try:
                    os.unlink(resFileName)
                except Exception:
                    pass

        
