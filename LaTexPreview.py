import sublime, sublime_plugin
from subprocess import Popen

import os

try:  # python 3
    from .functions import cutEquation, cutBlock, makeOutput, readPreamble, ENVIRON, fileDelete, FileProperties, workingFiles
except ValueError:  # python 2
    from functions import cutEquation, cutBlock, makeOutput, readPreamble, ENVIRON, fileDelete, FileProperties, workingFiles



def stopPrevew(fileName):

    global workingFiles

    if (fileName in workingFiles):
        currentProperties = workingFiles[fileName]
        currentProperties.isRun = False

        if (currentProperties.runProc != None):
            if (currentProperties.runProc.poll() == None):
                currentProperties.runProc.kill()

        if  (currentProperties.resFileName != None):
            fileDelete(currentProperties.resFileName)
            


def makeFile(view, cutFunction):
    sel = view.sel()[0]
    
    code = cutFunction(view)

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


def applicationReload(view, currentProperties):

    nResFileName = makeFile(view, currentProperties.cutFunction)

    if (nResFileName == None):
        return

    if (currentProperties.runProc != None):        
        if (currentProperties.runProc.poll() == None):
            currentProperties.runProc.kill()

    if (currentProperties.resFileName != None):
        while ((os.path.exists(currentProperties.resFileName))):
            fileDelete(currentProperties.resFileName)

    currentProperties.resFileName = nResFileName
   
    try:
        pdf_open_app = sublime.load_settings("TeXPreview.sublime-settings").get("pdf_open_app")
        currentProperties.runProc = Popen((pdf_open_app + " " + str(currentProperties.resFileName)).split(), env=ENVIRON)
        
    except Exception as e:
        sublime.error_message('LaTeX Preview: Could not open the file! '+ str(currentProperties.resFileName))
        raise e

    currentProperties.isRun = True

def changePic(view, currentProperties):
    
    nResFileName = makeFile(view, currentProperties.cutFunction)

    if (nResFileName == None):
        return 
    try:
        os.remove(currentProperties.resFileName)
        os.rename(nResFileName, currentProperties.resFileName)

    except Exception as e:
        os.remove(nResFileName)
        
        #sublime.error_message('LaTeX Preview: Could not change the file! ' +  str(currentProperties.resFileNameresFileName))
        #raise e


class LatexPreviewEvent(sublime_plugin.EventListener):
    
    def on_selection_modified_async(self, view):

        global workingFiles

        fileName = view.file_name()

        if not(fileName in workingFiles):
            return

        currentProperties = workingFiles[fileName]

        
        if ((currentProperties.runProc != None) and (currentProperties.runProc.poll() != None)):
            currentProperties.runProc = None
            currentProperties.isRun = False

            if ((os.path.exists(currentProperties.resFileName))):
                fileDelete(currentProperties.resFileName)
                return

        if (currentProperties.isRun == False):
            return

        auto_reload = sublime.load_settings("TeXPreview.sublime-settings").get("auto_reload") 

        if (auto_reload == False):
            return

        if (auto_reload == "application_reload"):
            applicationReload(view, currentProperties)
            return

        changePic(view, currentProperties)
        

    def on_load_async(self, view):
        ENVIRON['PATH'] += sublime.load_settings("TeXPreview.sublime-settings").get("latex_path")

        

    def on_pre_close(self, view):

        fileName = view.file_name()
        stopPrevew(fileName)


class LatexPreviewCommand(sublime_plugin.TextCommand):

    def run(self, view):
        fileName = self.view.file_name()

        if (fileName == None):
            return
        if (fileName[-4:] != '.tex'):
            return
             
        global workingFiles

        if not(fileName in workingFiles):
            workingFiles[fileName] = FileProperties()

        currentProperties = workingFiles[fileName]
        currentProperties.isRun = True
        currentProperties.cutFunction = lambda x:cutEquation(x)
        applicationReload(self.view, currentProperties)
            

class LatexBlockPreviewCommand(sublime_plugin.TextCommand):

    def run(self, view):
        fileName = self.view.file_name()

        if (fileName == None):
            return
        if (fileName[-4:] != '.tex'):
            return

        global workingFiles

        if not(fileName in workingFiles):
            workingFiles[fileName] = FileProperties()

        currentProperties = workingFiles[fileName]
        currentProperties.isRun = True
        currentProperties.cutFunction = lambda x:cutBlock(x)
        applicationReload(self.view, currentProperties)


class LatexStopPreviewCommand(sublime_plugin.TextCommand):
    def run(self, view):

        fileName = self.view.file_name()
        stopPrevew(fileName)

        
        
