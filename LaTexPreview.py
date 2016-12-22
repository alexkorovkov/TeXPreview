import sublime, sublime_plugin

try:  # python 3
    from .functions import *
    from .openfunctions import *
except ValueError:  # python 2
    from functions import *
    from openfunctions import *

def plugin_loaded():
    ENVIRON['PATH'] += str(
                           sublime.load_settings("TeXPreview.sublime-settings").get("latex_path")
                           )
    print("Your path for TeXPrevew:", ENVIRON['PATH'])

class LatexPreviewEvent(sublime_plugin.EventListener):
    
    def on_selection_modified_async(self, view):

        global workingFiles

        fileName = view.file_name()

        if not(fileName in workingFiles):
            return

        currentProperties = workingFiles[fileName]

        if (sublime.load_settings(
            "TeXPreview.sublime-settings"
            ).get("external_view") == False):
                sublime_open(view, currentProperties)
                return 
        
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
        

    #def on_load_async(self, view):
    #    ENVIRON['PATH'] += sublime.load_settings("TeXPreview.sublime-settings").get("latex_path")

        

    def on_pre_close(self, view):

        fileName = view.file_name()
        stopPrevew(fileName)

        dirPath = os.path.dirname(view.file_name())+os.path.sep +r'TeX_Preview_tmp'

        if ((os.path.exists(dirPath))):
            try:
                os.rmdir(dirPath)
            except:
                pass


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
        currentProperties.code = None
        currentProperties.isRun = True
        currentProperties.cutFunction = lambda x:cutEquation(x)
        if (sublime.load_settings(
            "TeXPreview.sublime-settings"
            ).get("external_view") == False):
            sublime_open(self.view, currentProperties)
        else:
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
        currentProperties.code = None
        currentProperties.isRun = True
        currentProperties.cutFunction = lambda x:cutBlock(x)
        if (sublime.load_settings(
            "TeXPreview.sublime-settings"
            ).get("external_view") == False):
            sublime_open(self.view, currentProperties)
        else:
            applicationReload(self.view, currentProperties)


class LatexStopPreviewCommand(sublime_plugin.TextCommand):
    def run(self, view):

        fileName = self.view.file_name()
        stopPrevew(fileName)

        self.view.window().destroy_output_panel("tex_pr_exec")

        
        
