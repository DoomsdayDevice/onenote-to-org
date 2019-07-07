from oto.import_file import import_file
from oto.parser import *
from oto.convert_to_org import convert_to_org
from oto.utils import filter_html, map_hierarchy

def convert_html_to_abstraction(source_file):
    list_of_lines = []
    initial_parser = InitialHTMLParser()
    initial_parser.feed(source_file, list_of_lines)

    for line in list_of_lines:
        PTagParser().feed(line.par, line)
        print("------PAR DONE -------")
        print("SENTENCES:", line.sentences)

    map_hierarchy(list_of_lines)

    return list_of_lines

def main():
    source_file = import_file()
    source_file = filter_html(source_file)

    list_of_lines = convert_html_to_abstraction(source_file)
    org_text = convert_to_org(list_of_lines) # convert python abstraction to org-mode format

    with open('output/oto-result.org', 'w', encoding='utf-8') as fobj:
        print(org_text, file=fobj)

    print("Success!")

if __name__ == "__main__":
    main()
