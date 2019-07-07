from html.parser import HTMLParser

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
