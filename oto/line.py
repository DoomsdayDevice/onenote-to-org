from .utils import get_substr, get_margin_left

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

