A python script that converts html files exported from Onenote to Emacs Org-mode format.  
*Work in progress*.

- Export .mht file(s) from Onenote (Note that collapsed entries won't be exported, you have to expand them)
- Convert .mht to .htm using Internet Explorer
- Point to .htm file(s) them like so:  
`python oto.py input/*.htm output_folder`  
or  
`python oto.py input/onenote_page.htm output_folder`  

Pass the `--divide` flag if you are importing an entire notebook with many pages and want to break it into multiple pages.

**Planned Features**: 
- Support for tables
- taking styles (like highlighting) into account when converting
