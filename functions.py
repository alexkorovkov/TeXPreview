from subprocess import Popen, PIPE
import os
import re
import tempfile
import sublime

ENVIRON = os.environ

EQUATION_COMPILE = re.compile(r'\\begin\{\s*(?:align|alignat|aligned|alignedat|displaymath|displaymath|eqnarray|equation|flalign|gather|gathered|math|multline|xalignat)\*?\}\s*(?s).+?\\end\{\s*.+?\}|\$\$.+?\$\$|\$.+?\$|\\\[.+?\\\]|\\\(.+?\\\)')

LaTeX_PREAMBULE = re.compile(r'\\documentclass.*?\{.+?\}(?s).+?\\begin\{document\}')
DOCUMENT_CLASS_RE = re.compile(r'\\documentclass.*?\{.+?\}')

def surroundingTeXEquation(data, cursor):
    '''
    Find LaTeX equation in source surrounding the cursor.
    '''
    
    equations = EQUATION_COMPILE.finditer(data)

    for m in equations:
        if ((m.start() <= cursor) and (m.end() >= cursor)):
            return(m.group(0))
        if (m.start() > cursor):
            return None

    return None

def  readPreambule(data):
    '''
    Find LaTeX preambule
    '''

    preambule = LaTeX_PREAMBULE.search(data)
    if (preambule == None):
        return ""
    else:
        #preambule = DOCUMENT_CLASS_RE.sub('\documentclass[convert={density=600,size=200x200,outext=.png},preview]{standalone}', preambule.group(0))
        preambule = DOCUMENT_CLASS_RE.sub('\documentclass[preview]{standalone}', preambule.group(0))
        return preambule

    return ""


def makeOutput(code, preambule, tmpDir):
    '''
    Convert LaTeX code
    '''

    tmpDir = tmpDir + os.path.sep +r'TeX_Preview_tmp'
    if not os.path.exists(tmpDir):
        os.makedirs(tmpDir)
    os.chdir(tmpDir)

    settings = sublime.load_settings("TeXPreview.sublime-settings")
    default_preambule = settings.get("default_preambule")
    pdf_latex_compiller = settings.get("pdf_latex_compiller")

    # temporary LaTeX file
    if (preambule == None):
       code = r'\documentclass[preview]{standalone}' + default_preambule +r'\begin{document}'+code+r'\end{document}'
    else: 
        code = preambule+code+r'\end{document}'

    
    eqfile = tempfile.NamedTemporaryFile(prefix='sublime_text_latex_', dir=tmpDir, suffix='.tex', delete=False, mode='wb')

    eqfile.write(code.encode('utf-8'))
    eqfile.close()

    # make pdf
    res_filename = os.path.splitext(eqfile.name)[0] +'.pdf'
    
    #for hide cmd in windows
    if (os.name == 'nt'):
        Popen([pdf_latex_compiller,'-interaction=nonstopmode','-shell-escape', eqfile.name], shell=True, env=ENVIRON).wait()
    else:
        Popen([pdf_latex_compiller,'-shell-escape', eqfile.name], shell=False, env=ENVIRON).wait()
    
    
    

    fileExt = [".tex", ".aux", ".log", ".out"]

    for ext in fileExt:
        if ((os.path.exists(os.path.splitext(eqfile.name)[0] +ext))):
            os.unlink(os.path.splitext(eqfile.name)[0] + ext)

    if ((os.path.exists(res_filename))):
        return res_filename

    return None