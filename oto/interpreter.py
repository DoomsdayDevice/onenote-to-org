import string
from . import utils
from .link import Link

class Interpreter:
    def __init__(self, list_of_lines):
        # list of all the line objects
        my_lines = []
        self.list_of_lines = list_of_lines
        self.hierarchy_map = ["0"]
        self.hierarchy_mapper()

        for line in self.list_of_lines:
            self.parse(line)

    def hierarchy_mapper(self):
        # takes style margins, stores them if they're no already in the list, then sorts the resulting array
        counter = 0
        number = ""
        # shorthand
        mylist = self.list_of_lines
        for index, line in enumerate(mylist):
            # look for margin, then count to 3 and on 4th append the number
            #
            for index, char in enumerate(line.get_par()):
                if line.get_par()[index:index+7] == "MARGIN:":
                    # now start counting numbers and when get to 4th - record it, if hit " or ; early - break
                    for i in range(index, len(line.get_par())):

                        if line.get_par()[i] in string.digits and (line.get_par()[i - 1] not in string.digits) and counter < 4:
                            counter += 1
                        if counter == 4 and (line.get_par()[i] in string.digits or line.get_par()[i] == "."):
                            number += line.get_par()[i]
                        if line.get_par()[i] in [';', '"']:
                            if number not in self.hierarchy_map and number != "":
                                self.hierarchy_map.append(number)
                                number = ""
                                counter = 0
                            break
                        # sorting the resulting map
        self.hierarchy_map.sort()
        print("the hierarchy map is:", self.hierarchy_map)

    def parse(self, line):
        # initial parsing that puts full style, img, <a>, tags inside their own strings
        # takes a line, breaks it into sub-strings and attaches those to corresponding line objects

        # iterate through the list, two vars: pointer and mode
        # get the style first, then img if it exists, then text inside <p>
        self.collect_style_pool(line)
        self.collect_img_pool(line)
        self.remove_nbsp(line)

        self.collect_stncs(line)
        self.style_parse(line)


    def collect_style_pool(self, line):
        # loop for style; copy all style into its own string, cut the line at >
        appending = False
        style_pool = ""
        for index, char in enumerate(line.get_par()):
            if line.get_par()[index-7:index] == 'style="':
                appending = True
            if char == '"':
                appending = False
            if appending:
                style_pool += char
            if not appending and char == ">":
                # removing the the <p> and </p> tags and what's inside, then breaking out of the loop
                line.set_par(line.get_par()[index+1:-4])
                break
            line.set_style_pool(style_pool)

    def collect_img_pool(self, line):
        #takes <img> contents, sends to checkbox analysis, removes from the paragraph
        appending = False
        img_pool = ""
        index_pos = -1
        for index, char in enumerate(line.get_par()):
            if line.get_par()[index:index+4] == "<IMG":
                appending = True
            if appending:
                img_pool += char
                if char == ">": # if we hit the end of img
                    appending = False
                    index_pos = index
                    break
                # removing <img> from the paragraph
        line.set_par(line.get_par()[index_pos+1:])

    def remove_nbsp(self, line):
        # removes all line-objects whose paragraph is "nbsp"
        # takes paragraph and removes all the instances of "&nbsp"
        # !!! problem: multiple nbsps
        # solution: remove it and move index back where started OR skip till after the thing
        new_paragraph = ""
        appending = True
        # counter skips symbols for &nbsp;
        counter = 0
        for i in range(len(line.get_par())):
            if line.get_par()[i:i+6] =="&nbsp;":
                appending = False
                counter = 6
            if not appending and counter == 0:
                appending = True
            if counter > 0:
                counter -= 1
            if appending:
                new_paragraph += line.get_par()[i]

        # removing newlines
        new_paragraph = new_paragraph.replace('\n  ', '')
        line.set_par(new_paragraph)


    def collect_stncs(self, line):
        # collects all sentences and linkspp

        #uses recursion
        def iterative_collect(paragraph):
            # until there's something left -
            new_paragraph = paragraph
            list_of_sents = []
            new_string = ''
            cut_prematurely = False
            while new_paragraph != '':
                if new_paragraph[0:2] == "<A":
                    for index, char in enumerate(new_paragraph):
                        if new_paragraph[index-2:index] == "/A>":
                            cut_prematurely = True
                            index_pos = index
                            break
                        new_string += char
                        # convert the string to a link object
                    new_string = Link(new_string)
                elif new_paragraph[0:5] == "<SPAN":
                    # UNFINISHED, i haven't implemented bold yet
                    # find > and append till </SPAN
                    for i in range(len(new_paragraph)):
                        if new_paragraph[i] == '>':
                            for j in range(i+1, len(new_paragraph)):
                                if new_paragraph[j] == '<':
                                    break
                                new_string += new_paragraph[j]
                            break

                    # find the end of </span> and cut it there
                    for index, char in enumerate(new_paragraph):
                        if new_paragraph[index-7:index] == "</SPAN>":
                            cut_prematurely = True
                            index_pos = index
                            break

                else:
                    for index, char in enumerate(new_paragraph):
                        if char == '<':
                            cut_prematurely = True
                            index_pos = index
                            break
                        new_string += char
                        list_of_sents.append(new_string)
                if cut_prematurely:
                    new_string = ''
                    cut_prematurely = False
                    new_paragraph = new_paragraph[index_pos:]
                else:
                    new_paragraph = ''
            return list_of_sents

        def recursive_collect(paragraph):
            # new string that will be added to the list of sents along with others
            new_string = ""
            # checks if link or not
            # adds the pool to a link object
            cut_prematurely = False
            if paragraph[0:2] == "<A":
                for index, char in enumerate(paragraph):
                    if paragraph[index-2:index] == "/A>":
                        cut_prematurely = True
                        break
                    new_string += char
                    # convert the string to a link object
                new_string = Link(new_string)
            else:
                for index, char in enumerate(paragraph):
                    if char == "<":
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

        # checkbox_id = "mht97B(1).tmp"
        # for index, char in enumerate(line.get_par()):
        #     if line.get_par()[index:index+4] == "<IMG":
        #         line.set_checkbox("unchecked")
        #         for i in range(index, len(line.get_par())):
        #             if line.get_par()[i:i+len(checkbox_id)+1] == checkbox_id:
        #                 line.set_checkbox("checked")
        #                 break
        #             print(line.get_par()[i:i+len(checkbox_id)+1])
        #         break
        # print(line.get_checkbox())
        pass
