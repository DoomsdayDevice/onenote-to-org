from oto.import_file import import_file
from oto.parser import MyHTMLParser
from oto.convert_to_org import convert_to_org
from oto.utils import filter_html


def main():
    parser = MyHTMLParser()
    source_file = import_file()
    source_file = filter_html(source_file)


    # convert html into python abstraction
    list_of_lines = []
    parser.feed(source_file, list_of_lines) # mutates list_of_lines

    # convert python abstraction into org-mode format
    org_text = convert_to_org(list_of_lines)

    with open('output/oto-result.org', 'w', encoding='utf-8') as fobj:
        print(org_text, file=fobj)

    print("Success!")

if __name__ == "__main__":
    main()
