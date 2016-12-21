import sublime
from subprocess import Popen

try:  # python 3
    from .functions import *
except ValueError:  # python 2
    from functions import *

import os

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


            


def makeFile(view, currentProperties):
    sel = view.sel()[0]

    code = currentProperties.cutFunction(view)

    if (code == currentProperties.code):
        return None

    if not code:
        return None

    currentProperties.code = code

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

    if (currentProperties.runProc != None):        
        if (currentProperties.runProc.poll() == None):
            currentProperties.runProc.kill()

    if (currentProperties.resFileName != None):
        while ((os.path.exists(currentProperties.resFileName))):
            fileDelete(currentProperties.resFileName)

    nResFileName = makeFile(view, currentProperties)

    if (nResFileName == None):
        return

    currentProperties.resFileName = nResFileName

    try:
        pdf_open_app = sublime.load_settings("TeXPreview.sublime-settings").get("pdf_open_app")
        currentProperties.runProc = Popen((pdf_open_app + " " + str(currentProperties.resFileName)).split(), env=ENVIRON)
        
    except Exception as e:
        sublime.error_message('LaTeX Preview: Could not open the file! '+ str(currentProperties.resFileName) + '''\nPlease check your "pdf_open_app" application''')
        raise e

    currentProperties.isRun = True

def changePic(view, currentProperties):
    
    nResFileName = makeFile(view, currentProperties)

    if (nResFileName == None):
        return 
    try:
        os.remove(currentProperties.resFileName)
        os.rename(nResFileName, currentProperties.resFileName)

    except Exception as e:
        os.remove(nResFileName)
        
        #sublime.error_message('LaTeX Preview: Could not change the file! ' +  str(currentProperties.resFileNameresFileName))
        #raise e

def sublime_open(view, currentProperties):

    if (currentProperties.isRun == False):
        return

    nResFileName = makeFile(view, currentProperties)

    if (nResFileName == None):
        return

    if (currentProperties.resFileName != None):
        while ((os.path.exists(currentProperties.resFileName))):
            fileDelete(currentProperties.resFileName)

    currentProperties.resFileName = nResFileName
    
    output_view = view.window().create_output_panel("tex_pr_exec")

    output_view.set_syntax_file("Packages/Text/Plain text.tmLanguage")

    output_view_settings = output_view.settings()
    output_view_settings.set("line_numbers", False)
    output_view_settings.set("scroll_past_end", False)

    view.window().run_command("show_panel", {"panel": "output.tex_pr_exec"})

    currentProperties.phantom_set = sublime.PhantomSet(output_view, "tex_pr_exec")

    width, height = get_image_size(currentProperties.resFileName)

    windowWidth, windowHeight = output_view.viewport_extent()

    maxDiv = min((windowWidth-5)/width, (windowHeight)/height)
    

    height = height*maxDiv
    width = width*maxDiv

    currentProperties.phantoms = []

    currentProperties.phantoms.append(
        sublime.Phantom(
            output_view.full_line(0),
            '''
            <img src="file://''' + currentProperties.resFileName + '''" width="'''+ str(width) +'''" height = "'''+ str(height) +'''">
            ''',
            sublime.LAYOUT_INLINE
            )
        )

    currentProperties.phantom_set.update(currentProperties.phantoms)
    
    return

