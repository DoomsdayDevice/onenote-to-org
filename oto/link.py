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
