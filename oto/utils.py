import string

def remove_newlines(text):
    return ''.join(text.splitlines())

def filter_html(text):
    new_text = remove_newlines(text)
    new_text = new_text.replace('&nbsp;', '')
    # new_text = new_text.replace('&apos;', "'")

    return new_text

def get_substr(string, from_str, break_chars):
    result = ""
    for index, char in enumerate(string):
        if string[index:index+len(from_str)] == from_str:
            # now start counting numbers and when get to 4th - record it
            # if hit " or ; early - break
            result = get_substr_till(string[index+len(from_str):], break_chars)

    return result

def get_substr_till(string, break_chars):
    result = ""
    for i in range(len(string)):
        if string[i] in break_chars:
            break
        result += string[i]
    return result

def map_hierarchy(list_of_lines):
    """takes style margins, stores them if they're not already in the list,
    then sorts the resulting array"""

    # shorthand
    mylist = list_of_lines
    hierarchy_map = []
    for index, line in enumerate(mylist):
        margin_left = line.margin_left
        if margin_left not in hierarchy_map:
            hierarchy_map.append(margin_left)

    hierarchy_map.sort()
    print("the hierarchy map is:", hierarchy_map)
    for line in mylist:
        line.offset = hierarchy_map.index(line.margin_left)

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
