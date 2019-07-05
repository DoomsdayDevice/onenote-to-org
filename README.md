A python script that converts html files exported from Onenote to Emacs Org-mode format.  
*Work in progress*. Only partially usable.

- Export .mht file(s) from Onenote
- convert .mht to .htm using Internet Explorer
- Point to .htm file(s) or folder containing them like so: 
`python oto.py input output_folder`
or
`python oto.py input/onenote_page.htm output_folder`



pass the `--divide` flag if you are importing an entire notebook with many pages

**Current State**: refactoring spaghetti code
**Up Next**: taking styles (like highlighting) into account when converting
