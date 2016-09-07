# TeXPreview
Sumlime Text plugin for preview TeX(LaTeX) equations.

This is a simple plugin that can help you to prevew your TeX (or LaTeX) equations. 

This plugin can do these:
-   View an equation in an external program (you can change it using `Preferences -> Package Settings -> TexPreview` menu)
-   Monitor for changing an equation while you are writting it (unfortunatelu Windows doesn't support it well)
-   Open and close an external program

To view an equation you shold set the cursor in TeX equation code and run "latex_preview" command.

TeXPreview commands
==========
To run and stop TeXPreview plugin you should use the following shortcut 

    [
      {
        "keys": ["ctrl+l"],
        "command": "latex_preview"
      },
      {
        "keys": ["ctrl+shift+l"],
        "command": "latex_stop_preview"
      }
    ]

You can change it using `Preferences -> Package Settings -> TexPreview` menu.

TeXPreview options
==========
Examples for TeXPreview options for Linux platform:
- "latex_path" - path to your pdf latex compiller
```  
   "latex_path": ":/usr/local/bin"
```
- "pdf_latex_compiller" - pdf latex compiller
``` 
 "pdf_latex_compiller": "pdflatex"
``` 
- "pdf_open_app" - external program for opening result .pdf file with an equation
``` 
  "pdf_open_app": "okular"
``` 
- "always_load_preambule" [true, false] - option to load your .tex file preambule every time when you build your equation via pdflatex compiller
```
  "always_load_preambule": false
```
- "load_preambule_after_error" [true, false] - optin to load preambule if .pdf file isn't exist 
```
  "load_preambule_after_error": true
```
- "default_preambule" - preambule that will add in a temporary tex file
```
  "default_preambule": "\\newcommand{\\Al}{{\\alpha}}"
```
- "auto_reload" ["application_reload", "file_reload", false, true] - variants to use the plugin. "application_reload" variant will reopen an external application (works in every OS, but it takes a lot of time) on every changing of an equation, "file_reload" (or true) variant only replace .pdf file (works excelent on OS X (with default Skim.app) and Linux (with default Okular))  on every changing of an equation, false variant only copmile and open .pdf file.
```
  "auto_reload": "file_reload"
```
