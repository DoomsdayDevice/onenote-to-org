def result_par(line):
    res = ''
    res += '*' * (line.offset + 1)
    res += ' '
    for sent in line.sentences:
        res += str(sent)
    return res + '\n'

def convert_to_org(list_of_lines):
    text = ""
    paragraph = ''
    for line in list_of_lines:
        text += result_par(line)

    return text
