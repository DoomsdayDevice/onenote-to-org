import string
from . import utils
from .link import Link


class Interpreter:
    def __init__(self, list_of_lines):
        # list of all the line objects
        # my_lines = []
        self.list_of_lines = list_of_lines
        self.hierarchy_map = ["0"]
        self.hierarchy_mapper()

        for line in self.list_of_lines:
            self.parse_line(line)

    def hierarchy_mapper(self):
        """takes style margins, stores them if they're not already in the list,
        then sorts the resulting array"""

        # shorthand
        mylist = self.list_of_lines
        for index, line in enumerate(mylist):
            # look for margin, then count to 3 and on 4th append the number
            self.map_left_margin(line.get_par())
            #
            # sorting the resulting map
        self.hierarchy_map.sort()
        print("the hierarchy map is:", self.hierarchy_map)

    def map_left_margin(self, paragraph):
        margins = utils.get_substr(paragraph, "MARGIN:", [';', '"'])
        left_margin = utils.get_left_margin(margins)
        if left_margin not in self.hierarchy_map and left_margin != "":
            self.hierarchy_map.append(left_margin)


    def parse_line(self, line):
        """ initial parsing that puts full style, img, <a>, tags inside their own strings
        takes a line, breaks it into sub-strings and attaches those to corresponding line objects

        iterate through the list, two vars: pointer and mode
        get the style first, then img if it exists, then text inside <p> """

        self.collect_style_pool(line)
        line.set_par(self.remove_p_tags(line.get_par()))

        self.collect_img_pool(line)
        self.remove_nbsp(line)

        self.collect_stncs(line)
        self.style_parse(line)


    def collect_style_pool(self, line):
        # loop for style; copy all style contents into their own string, cut the line at >
        style_start = "style=\""
        style_pool = utils.get_substr(line.get_par(), style_start, ['"'])

        line.set_style_pool(style_pool)

    @staticmethod
    def remove_p_tags(paragraph):
        return paragraph[paragraph.index('>')+1:-4]

    def collect_img_pool(self, line):
        """takes <img> contents, sends to checkbox analysis
        removes <img> tag from the paragraph"""
        img_start = "<IMG"
        img_pool = utils.get_substr(line.get_par(), img_start, ['>'])

        if img_pool != '':
            # removing <img> tag from the paragraph
            par = line.get_par()
            new_par = par[par.index('>')+1:]
            line.set_par(new_par)

    def remove_nbsp(self, line):
        """ removes all line-objects whose paragraph is "nbsp"
        takes paragraph and removes all the instances of "&nbsp"
        TODO: problem when multiple nbsps
        solution: remove it and move index back where started OR skip till after the thing """

        new_paragraph = ""
        # counter skips symbols for &nbsp;
        new_paragraph = utils.remove_substr(line.get_par(), "&npsp;")

        # removing newlines
        new_paragraph = new_paragraph.replace('\n  ', '')
        line.set_par(new_paragraph)


    def collect_stncs(self, line):
        # collects all sentences and links

        # uses recursion
        def iterative_collect(par):
            pass

        def recursive_collect(paragraph):
            # new string that will be added to the list of sents along with others
            new_string = ""
            cut_prematurely = False
            if utils.starts_with_link(paragraph): # if paragraph stats with a link
                end_of_link = paragraph.index("/A>") + 3 + 1
                new_string = paragraph[:end_of_link]
                index = end_of_link

                new_string = Link(new_string)

                if end_of_link != len(paragraph):
                    cut_prematurely = True
            else: # if it's just text
                for index, char in enumerate(paragraph):
                    if char == "<": # if stumble upon another tag
                        cut_prematurely = True
                        break
                    new_string += char
                    # breaks if hits a link

            # if the end: returns just a string, if not - extends with output from the next function call
            list_of_sents = []
            list_of_sents.append(new_string)
            # if we cut prematurely - means there's something else left
            if cut_prematurely:
                cut_paragraph = paragraph[index:]

                list_of_sents.extend(recursive_collect(cut_paragraph))
                return list_of_sents
            else:
                return list_of_sents


        # line.set_sentences(iterative_collect(line.get_par()))
        line.set_sentences(recursive_collect(line.get_par()))

    # final parses
    def style_parse(self, line):
        # takes an initial style pool, takes margin and one of 3 highlights and converts them to the object
        def determine_margin(pool):
            # find margin in text and look for the fourth number OR if hits ; - count as 0
            margin = "0"
            count = 0
            for index, elem in enumerate(pool):
                if pool[index:index+6] == "MARGIN":
                    # once margin is found - start iterating pool from there
                    margin = ''
                    for i in range(index, len(pool)):
                        # count numbers until count to 3 and record the next one
                        # if hits ; - break and
                        if count == 3 and (pool[i] in string.digits or pool[i] == '.'):
                            margin += pool[i]
                        if (pool[i] in string.digits) and (pool[i-1] not in string.digits) and count < 3:
                            count += 1
                        if pool[i] == ';':
                            break
                    if count < 3:
                        margin = '0'
                    break
            return margin


        def determine_style(pool):
            # if contains bg - start appending until hit ;
            # appends everything excent "background"
            background = utils.copy_everything_from_except(pool, "BACKGROUND: ", ';')

            # look for COLOR
            color = ""
            i = 0
            appending = False
            color = utils.copy_everything_from_except(pool, "COLOR: ", ';')

            if background == "#00ccff":
                return "special"

            elif color == "#ff99cc":
                return "uncertain"

            elif background == "lime":
                return "important"

            elif False:
                # UNFINISHED finish this later
                return "bold"

            else:
                return ""


        # setting the position in the hierarchy based on the margin
        line.set_hierarchy(self.hierarchy_map.index(determine_margin(line.style_pool)))
        line.set_style(determine_style(line.style_pool))


    def checkbox_parse(self):
        # takes the initial <img> pool and interprets it into the checkbox value

        # loop for img; impossible to ID right now, because the image name is diff every time
        # gotta analyze the image itself
        pass
