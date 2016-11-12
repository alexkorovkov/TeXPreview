from subprocess import Popen, PIPE
import os
import re
import tempfile
import sublime


ENVIRON = os.environ

EQUATION_SELECTOR = "meta.environment.math"
BLOCK_SELECTOR = "meta.environment.math.block.be.latex"

LATEX_BEGIN_COMPILE = re.compile(r'\\begin\{\s*.+?\}')
LATEX_END_COMPILE = re.compile(r'\\end\{\s*.+?\}')
LATEX_BLOCK_COMPILE = re.compile(r'\\begin\{\s?(?P<block>(?!document)\w*?|)\W*?\}(\s|.)*?\\end\{\s??(?P=block)\W*?\}')

LaTeX_Preamble = re.compile(r'\\documentclass.*?\{.+?\}(?s).+?\\begin\{document\}')
DOCUMENT_CLASS_RE = re.compile(r'\\documentclass.*?\{.+?\}')

workingFiles = dict()

class FileProperties:
    """Class for current file properties"""
    def __init__(self):
        self.isRun = None
        self.resFileName = None
        self.runProc = None
        self.cutFunction = None

def cutEquation(view):
    '''
    Find LaTeX equation in source surrounding the cursor.
    '''
    
    position = view.sel()[0].begin() #only the first one

    isInEquation = lambda pos: view.match_selector(pos, EQUATION_SELECTOR)

    if (isInEquation(position)):
        
        startPosition = position
        while (isInEquation(startPosition) or startPosition < 0):
            startPosition -= 1

        fileLen = view.size()
        endPosition = position
        while (isInEquation(endPosition) or endPosition > fileLen):
            endPosition += 1

        if (view.match_selector(position, BLOCK_SELECTOR)):

            lineStartPosition = view.full_line(startPosition).begin()

            startPosition = lineStartPosition + LATEX_BEGIN_COMPILE.search(
                view.substr(sublime.Region(
                    lineStartPosition, 
                    startPosition+1))
                ).start()

            endPosition += LATEX_END_COMPILE.match(
                view.substr(sublime.Region(endPosition, fileLen))
             ).end()

        return(view.substr(sublime.Region(startPosition+1, endPosition)))
                
    return None

def cutBlock(view):
    '''
    Find LaTeX equation in source surrounding the cursor.
    '''

    position = view.sel()[0].begin() #only the first one

    data = LATEX_BLOCK_COMPILE.finditer(
            view.substr(sublime.Region(0, view.size()))
        )
    
    for m in data:
        if ((m.start() <= position) and (m.end() >= position)):
            return(m.group(0))
        if (m.start() > position):
            return view.substr(view.full_line(position))

    return None

def  readPreamble(data, external_view_flag = True):
    '''
    Find LaTeX preamble
    '''

    preamble = LaTeX_Preamble.search(data)
    if (preamble == None):
        return ""
    else:
        if (external_view_flag == False):
            tmpStr = "convert={density=600,outext=.png},"
        else:
            tmpStr = ""
        preamble = DOCUMENT_CLASS_RE.sub('\documentclass[' + tmpStr + 'preview]{standalone}', preamble.group(0))
        return preamble

    return "" 

def makeOutput(code, preamble, tmpDir):
    '''
    Convert LaTeX code
    '''

    tmpDir = tmpDir + os.path.sep +r'TeX_Preview_tmp'
    if not os.path.exists(tmpDir):
        os.makedirs(tmpDir)
    os.chdir(tmpDir)

    settings = sublime.load_settings("TeXPreview.sublime-settings")
    default_preamble = settings.get("default_preamble")
    pdf_latex_compiler = settings.get("pdf_latex_compiler")

    if (preamble == None):
        preamble = r'\documentclass[preview]{standalone}' + default_preamble +r'\begin{document}'


    fileExt = [".tex", ".aux", ".log", ".out"]

    eqfile = tempfile.NamedTemporaryFile(prefix='sublime_text_latex_', dir=tmpDir, suffix='.tex', delete=False, mode='wb')


    if (settings.get("external_view") == False):
        preamble = readPreamble(preamble, False)
        fileExt.append(".pdf")
        res_filename = eqfile.name[:-4] +'.png'
        
    else:
        res_filename = eqfile.name[:-4] +'.pdf'

    code = preamble+code+r'\end{document}'

    eqfile.write(code.encode('utf-8'))
    eqfile.close()

    

    #for hiding cmd in windows
    if (os.name == 'nt'):
        Popen([pdf_latex_compiler,'-interaction=nonstopmode','-shell-escape', eqfile.name], shell=True, env=ENVIRON).wait()
    else:
        Popen([pdf_latex_compiler,'-shell-escape', eqfile.name], shell=False, env=ENVIRON).wait()
    

    for ext in fileExt:
        tempFileName = eqfile.name[:-4] + ext
        if (os.path.exists(tempFileName)):
            os.unlink(tempFileName)

    if ((os.path.exists(res_filename))):
        return res_filename

    return None


def fileDelete(fileName):
    while ((os.path.exists(fileName))):
        try:
            os.unlink(fileName)
        except Exception:
            pass