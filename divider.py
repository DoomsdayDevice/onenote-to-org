import string


class Importer:

    def __init__(self):
        self.source = ""
        self.output_folder = "divider_output"
        
        self.read_config()
        self.import_text()
        # cut, put into Exporter
        self.cutter()
        


    def read_config(self):
        with open("config", 'r') as fobj:
            text = fobj.read()
            appending = False
            pointer = ''

            block_id = "[divider]"
            def find_block(text, block_id):
                # looking for block start
                for i in range(len(text)):
                    if text[i:i+len(block_id)] == block_id:
                        block_start = i+len(block_id)
                        break
                # looking for block end
                for i in range(block_start, len(text)):
                    if text[i] == '[':
                        block_end = i-1
                        break
                    block_end = i
                return (block_start, block_end)
            
            block_start, block_end = find_block(text, block_id)

            index = block_start
            while index <= block_end:
                char = text[index]
                if appending:
                    if text[index+1] == '"':
                        appending = False
                    exec(pointer + " += char")
                if text[index:index+7] == "source=" and text[index+9] != '"':
                    pointer = "self.source"
                    self.source = ""
                    appending = True
                    index = index + 7
                if text[index:index+7] == "output=" and text[index+9] != '"':
                    pointer = "self.output_folder"
                    self.output_folder = ""
                    appending = True
                    index = index + 7
                index += 1
            print("source:", self.source)
            print("output folder:", self.output_folder)

    
    def import_text(self):
        with open(self.source, 'r') as fobj:
            self.text = fobj.read()

    def cutter(self):
        # iterates through the text
        # finds division lines
        # marks as beginning - the next as end
        # cuts text, passes to Exporter class
        # assigns beginning as end, looks for the next one
        # repeat
        divider = '<DIV style="DIRECTION: ltr">'
        index = 0
        beginning = 0
        end = 0
        while index < len(self.text):
            print("heeh")
            if self.text[index:index+len(divider)] == divider:
                if beginning == 0:
                    beginning = index
                else:
                    end = index
                    print("exportan")
                    Exporter(self.text[beginning:end], self.output_folder)
                    beginning = end
            index += 1

class Exporter:
    previous_name = "Originallio"
    current_file = 1

	
    # looks for name
    def __init__(self, text, output_folder):
        print(text)
        self.text = text
        self.output_folder = output_folder
        
        self.name_lookup()
        if self.appendage:
            self.export_text_append()
        else:
            self.export_text()

    def export_text(self):
        filename = self.output_folder + "/" + str(Exporter.current_file) + ' ' + self.name + ".html" 
        Exporter.previous_name = filename
        with open(filename , "w") as fobj:
            print(self.text, file=fobj)
        Exporter.current_file += 1
    def export_text_append(self):
        filename = Exporter.previous_name
        # logging which file has been appended where
        with open(self.output_folder + '/' + "#-appendage-logs.txt", 'w') as fobj:
            print("appended to :", Exporter.previous_name, file=fobj)
        # appending
        with open(filename, 'a') as fobj:
            print(self.text, file=fobj)
                        
    def name_lookup(self):
        # if the first P doesn't have Calibri light - use the static name
        def look_for_first_par():
            for i in range(len(self.text)):
                if self.text[i:i+2] == "<P":
                    beginning = i
                    for j in range(i, len(self.text)):
                        if self.text[j:j+4] == "</P>":
                            end = j+4
                            break
                    break
            return self.text[beginning:end]

        def get_name(paragraph):
            # if font Calibri Light - print
            # when find > - assign index to start - when find the next < - assign to end
            def get_rid_of_chars(name):
                # removes newlines and replaces backslashes from the name
                new_name = ""
                for index, char in enumerate(name):
                    if char == '/':
                        new_name += ':'
                    elif char == "\n":
                        continue                    
                    else:
                        new_name += char
                return new_name
                        
            start = 0
            end = 0
            for i in range(len(paragraph)):
                if paragraph[i] == '>':
                    start = i+1
                    for j in range(i, len(paragraph)):
                        if paragraph[j] == '<':
                            end = j
                            break
                    break
            name = paragraph[start: end]
            name = get_rid_of_chars(name)
            return name

        def has_calibri(paragraph):
            string = "Calibri Light"
            for i in range(len(paragraph)):
                if paragraph[i:i+len(string)] == string:
                    return True
        # if cannot find the headline - use the static var, previous name
        paragraph = look_for_first_par()
        
        if has_calibri(paragraph):
            self.appendage = False
            self.name = get_name(paragraph)
        else:
            self.appendage = True
                
        
        

def main():
    Importer()
    print("Success!")

if __name__ == "__main__":
    main()
