import os

from oto.import_file import import_file
from oto.parser import *
from oto.convert_to_org import convert_to_org
from oto.utils import filter_html, map_hierarchy
from oto.configure import configure

def convert_html_to_abstraction(source_file):
    list_of_lines = []
    initial_parser = InitialHTMLParser()
    initial_parser.feed(source_file, list_of_lines)

    p_tag_parser = PTagParser()
    for line in list_of_lines:
        p_tag_parser.feed(line.par, line)
        print("------PAR DONE -------")
        print("SENTENCES:", line.sentences)

    map_hierarchy(list_of_lines)

    return list_of_lines

def process_file(filename, output_folder):
    source_file = import_file(filename)
    source_file = filter_html(source_file)

    list_of_lines = convert_html_to_abstraction(source_file)
    org_text = convert_to_org(list_of_lines) # convert python abstraction to org-mode format

    filename_no_ext = os.path.splitext(os.path.basename(filename))[0]
    output_filename = '%s/%s.org' % (output_folder, filename_no_ext)
    with open(output_filename, 'w', encoding='utf-8') as fobj:
        print(org_text, file=fobj)

    print('Successfully converted ', filename)

def main():
    config = configure()

    for filename in config['list_of_files']:
        print("CURRENT FILENAME", filename)
        process_file(filename, config['output'])

    print("Success!")

if __name__ == "__main__":
    main()
