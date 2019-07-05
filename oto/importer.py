import sys
import os

from oto import utils
from oto.line import Line
from oto.link import Link

class Importer:
    """ Imports the html file and removes everything but <p> tags
    two modes: append, skip """

    def __init__(self):
        """ import file and append each paragraph to a list of strings """
        self.list_of_lines = []

        self.import_file = ""
        self.export_filename = ""
        self.export_folder = ""
        self.list_of_files = []


        self.read_args()
        self.list_of_imported_files = []
        for html_file in self.list_of_files:
            self.import_file = html_file
            filename = self.find_filename(self.import_file)
            filename = self.replace_html_with_org(filename)
            self.export_filename = self.export_folder + filename

            self.list_of_lines = self.initial_cut(self.import_file)
            # for line in self.list_of_lines:
            #     print(line.paragraph)
            # Interpreter(self.list_of_lines)
            self.list_of_imported_files.append(self.list_of_lines)

        # self.config()
        print("IMP:", self.import_file, " EXP:", self.export_filename)

    def get_files(self):
        return self.list_of_imported_files

    @staticmethod
    def initial_cut(import_file):
        """ takes the initial document and breaks into manageable pieces """
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
        print("import:", sys.argv[1], "Exp. folder:", sys.argv[2])
        self.import_file = sys.argv[1]
        self.export_folder = sys.argv[-1] # the last argument is the export folder
        if self.export_folder[-1] != '/': # in case no '/' was passed
            self.export_folder += '/'


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
                list_of_paths.append(new_list[0] + i)


        # take the name of the file and append to export
        for index, file_path in enumerate(list_of_paths): # check if it's an html file
            if file_path[-4:] == "html" or file_path[-3:] == "htm":
                self.list_of_files.append(file_path)


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

