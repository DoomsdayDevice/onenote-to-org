import string


class Filter:
    """ class that imports the html file and removes everything but p 
    two modes: append, skip """

    def __init__(self, filename):
        # import file and append each paragraph to a list of strings
        self.list_of_lines = []
        with open(filename, 'r') as fobj:
            text = fobj.read()
            cur_index = 0
            append = False
            for i in range(len(text)):
                if not append:
                    if text[i] == "<" and text[i+1] == "P":
                        append = True
                        # creating a new Line object and sending it the first character
                        self.list_of_lines.append(Line(text[i]))
                    else:
                        pass
                else:
                    if text[i-1] == ">" and text[i-4:i-1] == "</P":
                        append = False
                        cur_index += 1
                    else:
                        self.list_of_lines[cur_index].append_to_par(text[i])

        # removing the title and footer lines
        # for i in range(3):
        #     del self.list_of_lines[0]
        # self.list_of_lines.pop()
        


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

class Link:
    def __init__(self, link_pool):
        self.pool = link_pool
        self.description = ""
        self.url = ""

        self.disassemble_pool()
        
    def disassemble_pool(self):
        # print("the pool is ", self.pool)
        # everything from href=" to " goes to url
        appending = False
        for index, char in enumerate(self.pool):
            if appending:
                self.url += char
                if self.pool[index+1] == '"':
                    break
            elif self.pool[index-5:index+1] == 'href="':
                appending = True
        # print("the url is: ", self.url)
        
        appending = False
        # everything after > and before < goes to description
        for index, char in enumerate(self.pool):
            if appending:
                self.description += char
                if self.pool[index+1] == '<':
                    break
            elif self.pool[index] == '>':
                appending = True
        # print("the descritption is: ", self.description)
            
        
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
                            # print("countin")
                        if counter == 4 and (line.get_par()[i] in string.digits or line.get_par()[i] == "."):
                            number += line.get_par()[i]
                        if line.get_par()[i] in [';', '"']:
                            # print("we found the sole zero or the end of the line, the char is:", line[i])
                            # print("the num is: ", number)
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


        line.set_sentences(iterative_collect(line.get_par()))

            
            
        
    


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
            background = ""
            # look for background attach everything until ;
            appending = False
            i = 0
            while i < len(pool):
                if pool[i:i+12] == "BACKGROUND: ":
                    appending = True
                    i += 12
                if appending:
                    if pool[i+1] == ';':
                        appending = False
                    background += pool[i]
                i += 1

            
            # look for COLOR
            color = ""
            i = 0
            appending = False
            while i < len(pool):
                if pool[i:i+7] == "COLOR: ":
                    appending = True
                    i += 7
                if appending:
                    if pool[i+1] == ';':
                        appending = False
                    color += pool[i]
                i += 1
            
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
        

        # setting the position in the hierarchy based in the margin
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
        #                 print("we found the img")
        #                 line.set_checkbox("checked")
        #                 break
        #             print(line.get_par()[i:i+len(checkbox_id)+1])
        #         break
        # print(line.get_checkbox())
        pass

class Exporter:
    # takes the list of lines and prints them to a txt file
    
    def __init__(self, the_list, filename):
        self.the_list = the_list
        self.text = ""
        for line in the_list:
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
            if type(elem) == Link:
                self.text += '[[' + elem.url + '][' + elem.description + ']]'
            else:
                self.text += elem
        put_style()
        self.text += '\n'

    def export(self, filename):
        with open(filename, 'w') as fobj:
            print(self.text, file=fobj)
        


def main():
    filename_import = "sources/current/Tasks.html"
    filename_export = "sources/current/Tasks.org"
    
    
    myFilter = Filter(filename_import)
    # gets the text (p tags) from the filter and passes to the interpreter
    Interpreter(myFilter.list_of_lines)
    Exporter(myFilter.list_of_lines, filename_export)

    print("Success!")
    

if __name__ == "__main__":
    main()
