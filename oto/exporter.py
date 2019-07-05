from .link import Link
class Exporter:
    # takes the list of lines and prints them to a txt file

    def __init__(self, list_of_lines, filename):
        self.list_of_lines = list_of_lines
        self.text = ""

        for line in list_of_lines:
            self.print_line(line)

        self.export(filename)

    def print_line(self, line):
        def put_style():
            nonlocal line
            nonlocal self

            if line.style == "important":
                self.text += '!'
            elif line.style == "uncertain":
                self.text += '~'
            elif line.style == "special":
                self.text += '+'

        # put hierarchy
        if line.sentences and line.sentences[0]:
            for i in range(line.hierarchy+1):
                self.text += '*'
                self.text += ' '

        # UNFINISHED depending on checkbox value - put a todo value

        # apply style
        put_style()
        for elem in line.get_sentences():
            print(elem)
            if type(elem) == Link:
                self.text += '[[' + elem.url + '][' + elem.description + ']]'
            else:
                self.text += elem
                put_style()
                self.text += '\n'

    def export(self, filename):
        with open(filename, 'w', encoding="utf_8") as fobj:
            print(self.text, file=fobj)
