import sys
import os

from oto import divider
from oto import utils
from oto.line import Line
from oto.link import Link
from oto.interpreter import Interpreter
from oto.exporter import Exporter

class Importer:
    """ class that imports the html file and removes everything but p
    two modes: append, skip """

    def __init__(self):
        # import file and append each paragraph to a list of strings
        self.list_of_lines = []

        self.import_file = ""
        self.export_file = ""
        self.export_folder = ""
        self.list_of_files = []


        self.read_args()
        for html_file in self.list_of_files:
            self.import_file = html_file
            filename = self.find_filename(self.import_file)
            filename = self.replace_html_with_org(filename)
            self.export_file = self.export_folder + filename

            self.list_of_lines = self.initial_cut(self.import_file)
            self.send_stuff_further(self.list_of_lines, self.export_file)

        # self.config()
        print("IMP:", self.import_file, " EXP:", self.export_file)

    @staticmethod
    def initial_cut(import_file):
        with open(import_file, 'r', encoding="utf_8") as fobj:
            text = fobj.read()
            cur_index = 0
            append = False
            list_of_lines = []
            for i in range(len(text)):
                if not append:
                    if text[i] == "<" and text[i+1] == "P":
                        append = True
                        # creating a new Line object and sending it the first character
                        list_of_lines.append(Line(text[i]))
                    else:
                        pass
                else:
                    if text[i-1] == ">" and text[i-4:i-1] == "</P":
                        append = False
                        cur_index += 1
                    else:
                        list_of_lines[cur_index].append_to_par(text[i])
        return list_of_lines

    def read_args(self):
        print("the entire sys.argv:", sys.argv)
        print("import:", sys.argv[1], "Exp. folder:", sys.argv[2])
        self.import_file = sys.argv[1]
        self.export_folder = sys.argv[-1] # the last argument is the export folder


        print("THE NEW LIST: ", list(os.walk(sys.argv[1])))
        if ".htm" in sys.argv[1]:
            self.list_of_files.append(sys.argv[1])
        else:
            self.read_args_folder()
        # create a list of paths
    def read_args_folder(self):
        list_of_paths = []
        if len(sys.argv) > 3:
            print("ERROR: MORE THAN 3 ARGS")
        else:
            new_list = list(os.walk(sys.argv[1]))[0]
            for i in new_list[2]:
                list_of_paths.append(new_list[0]+ i)


        # take the name of the file and append to export
        for index, file_path in enumerate(list_of_paths): # check if it's an html file
            if file_path[-4:] == "html" or file_path[-3:] == "htm":
                self.list_of_files.append(file_path)
                print("file path:", file_path)


    @staticmethod
    def find_filename(filename):
        # finds the filename given a full path
        # find the last slash, if none - just copy
        slash_index = 0
        for index, char in enumerate(filename):
            if char == '/':
                slash_index = index + 1
        return filename [slash_index:]

    @staticmethod
    def replace_html_with_org(filename):
        if filename[-4:] == "html":
            return filename[:-4] + "org"
        elif filename[-3:] == "htm":
            return filename[:-3] + "org"

    @staticmethod
    def send_stuff_further(list_of_lines, export_file):
        Interpreter(list_of_lines)
        Exporter(list_of_lines, export_file)


    def config(self):
        block_id = "[converter]"
        def import_config():
            with open("config", 'r') as fobj:
                return fobj.read()
        def find_block(text, block_id):
            # looking for block start
            for i in range(len(text)):
                if text[i:i+len(block_id)] == block_id:
                    block_start = i+len(block_id)
                    break
                # looking for block end
            for i in range(block_start, len(text)):
                if text[i] == '[':
                    block_end = i-1
                    break
                block_end = i
            return (block_start, block_end)

        def find_source(text, BS, BE):
            # finding source
            for i in range(BS, BE):
                if text[i:i+len("source")] == "source":
                    print("we found source")
                    source_start = i+len("source")+2
                    for j in range(source_start, BE):
                        if text[j] == '"':
                            source_end = j
                            break
                    break
            return text[source_start:source_end]

        def find_output(text, BS, BE):
            # finding output
            for i in range(BS, BE):
                if text[i:i+len("output")] == "output":
                    output_start = i + len("output") + 2
                    for j in range(output_start, BE):
                        if text[j] == '"':
                            output_end = j
                            break
                    break
            return text[output_start:output_end]

        # find source location and attach to object

        text = import_config()
        block_start, block_end = find_block(text, block_id)
        self.import_file = find_source(text, block_start, block_end)
        self.export_file = find_output(text, block_start, block_end)

def main():
    myImporter = Importer()
    # gets the text (p tags) from the filter and passes to the interpreter

    print("Success!")


if __name__ == "__main__":
    main()
