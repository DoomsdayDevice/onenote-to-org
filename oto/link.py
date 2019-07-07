class Link:
    def __init__(self):
        self.text = ''
        self.href = ''

    def __str__(self):
        return '[[%s][%s]]' % (self.href, self.text)
