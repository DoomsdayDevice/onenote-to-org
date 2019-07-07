class Line:
    def __init__(self, char):
        self.paragraph = char
        self.style_pool = ""
        self.checkbox = ""
        self.sentences = []
        self.hierarchy = 0
        self.style = ""
    def append_to_par(self, char):
        self.paragraph += char

    def get_par(self):
        return self.paragraph

    def set_style_pool(self, pool):
        self.style_pool = pool

    def set_par(self, paragraph):
        self.paragraph = paragraph

    def set_checkbox(self, value):
        self.checkbox = value

    def get_checkbox(self):
        return self.checkbox

    def set_sentences(self, the_list):
        print("LIST OF STNCS:", the_list)
        self.sentences = the_list
    def get_sentences(self):
        return self.sentences

    def set_hierarchy(self, margin):
        self.hierarchy = margin
    def get_hierarchy(self):
        return self.hierarchy

    def set_style(self, style):
        self.style = style
    def get_style(self):
        return self.style
