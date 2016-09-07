# TeXPreview
Sumlime Text plugin for preview TeX(LaTeX) equations.

This is a simple plugin that can help you to preview your TeX (or LaTeX) equations. 

This plugin can do these:
- View an equation in an external program (you can change it using `Preferences -> Package Settings -> TexPreview` menu)
- Monitor for changing an equation while you are writing it (unfortunately Windows doesn't support it well)

To view an equation you should set the cursor in TeX equation code and run "latex_preview" command.

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
- "latex_path" - path to your pdf latex compiler
```  
   "latex_path": ":/usr/local/bin"
```
- "pdf_latex_compiler" - pdf latex compiler
``` 
 "pdf_latex_compiler": "pdflatex"
``` 
- "pdf_open_app" - external program for opening result .pdf file with an equation
``` 
  "pdf_open_app": "okular"
``` 
- "always_load_preamble" [true, false] - option to load your .tex file preamble every time when you build your equation via pdflatex compiler
```
  "always_load_preamble": false
```
- "load_preamble_after_error" [true, false] - option to load preamble if .pdf file isn't exist 
```
  "load_preamble_after_error": true
```
- "default_preamble" - preamble that will add in a temporary tex file
```
  "default_preamble": "\\newcommand{\\Al}{{\\alpha}}"
```
- "auto_reload" ["application_reload", "file_reload", false, true] - variants to use the plugin. "application_reload" variant will reopen an external application (works in every OS, but it takes a lot of time) on every changing of an equation, "file_reload" (or true) variant only replace .pdf file (works excelent on OS X (with default Skim.app) and Linux (with default Okular))  on every changing of an equation, false variant only compile and open .pdf file.
```
  "auto_reload": "file_reload"
```

