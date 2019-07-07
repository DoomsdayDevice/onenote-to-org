from .utils import get_substr
import string

def get_margin_left_from_str(margins):
    """ gets the value of the first number in the string
    or the fourth if there are four """
    number = ""
    counter = 0
    for i, char in enumerate(margins):
        if char in string.digits and (margins[i - 1] not in string.digits) and counter < 4:
            counter += 1
        if counter == 4 and (char in string.digits or margins[i] == "."):
            number += char
    left_margin = number
    return left_margin

def get_margin_left(style):
    res = ''
    res = get_substr(style, "MARGIN: ", [';', '"'])
    res = get_margin_left_from_str(res)
    if res == '':
        res = 0
    res = float(res)
    print ("THE MARGIN IS: ", res)
    return res

class Line:
    def __init__(self):
        self.par = ''
        self.margin_left = 0.0
        self.offset = 0
        self.style = ''
        self.sentences = []

    @property
    def style(self):
        return __style

    @style.setter
    def style(self, style):
        self.__style = style
        self.margin_left = get_margin_left(style)

