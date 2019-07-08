from html.parser import HTMLParser
from .line import Line
from .link import Link

class InitialHTMLParser(HTMLParser):
    """ takes all the <p> tags and puts them inside line objects """
    def feed(self, html, list_of_lines):
        self.list_of_lines = list_of_lines

        self.curr_p_start = 0
        self.curr_p_end = 0
        self.currentLine = 0
        self.text = html

        HTMLParser.feed(self, html)

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        if tag == 'p':
            print("Encountered P tag:", tag)
            self.curr_p_start = self.getpos()[1]

            self.list_of_lines.append(Line())
            # print("It has some attrs:", attrs)

    def handle_endtag(self, tag):
        print("Encountered an end tag:", tag)
        if tag == 'p':
            print("Encountered an end tag:", tag)
            self.curr_p_end = self.getpos()[1]

            start = self.curr_p_start
            end = self.curr_p_end + len('</P>')
            self.list_of_lines[self.currentLine].par = self.text[start:end]
            self.currentLine += 1
    def handle_data(self, data):
        print("Encountered some data:", data)

    def handle_entityref(self, name):
        print("ENC ENTITY REF:", name)


class PTagParser(HTMLParser):
    def feed(self, html, line):
        self.line = line
        self.current_tag = ''

        HTMLParser.feed(self, html)
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.line.style = attrs[0][1]
        elif tag == 'a':
            self.current_tag = 'a'
            self.current_link = Link()
            self.current_link.href = attrs[0][1]
        elif tag == 'span':
            # ignored for now and just appended to previous
            pass

        # self.current_tag = tag

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.current_tag == 'a':
            self.current_link.text += data
            self.line.sentences.append(self.current_link)
        else:
            self.line.sentences.append(data)


class MyHTMLParser(HTMLParser):
    def feed(self, html, list_of_lines):
        self.list_of_lines = list_of_lines
        HTMLParser.feed(self, html)

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        # print("It has some attrs:", attrs)

    def handle_endtag(self, tag):
        print("Encountered an end tag:", tag)

    def handle_data(self, data):
        print("Encountered some data:", data)
        self.list_of_lines.append(data + '\n')

    def handle_comment(self, data):
        print("Encountered some comment:", data)

    def handle_entityref(self, name):
        pass
