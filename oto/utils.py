import string

def copy_everything_from_except(pool, id_string, stop_symbol):
    """ copies contents of the string from the end of id_string till the stop_symbol """

    i = 0
    appending = False
    result = ""
    while i < len(pool):
        if pool[i:i+len(id_string)] == id_string:
            appending = True
            i += len(id_string)
        if appending:
            result += pool[i]
            if pool[i+len(stop_symbol)] == stop_symbol:
                appending = False
        i += 1
    return result

def get_index_of_next_char(text, start_index, char):
    """ returns the symbol of next ocurrence of a char starting at a specific point """
    index = 0
    for i in range(start_index, len(text)):
        if text[i] == char:
            index = i
            break
    return index

def get_start(text, substring):
    """ return the index substring where the substring starts """
    for i in range(len(text)):
        if text[i:i+len(substring)] == substring:
            start_index = i+len(substring)
            break
    return start_index


def get_substr(pool, from_str, break_chars):
    result = ""
    for index, char in enumerate(pool):
        if pool[index:index+len(from_str)] == from_str:
            # now start counting numbers and when get to 4th - record it
            # if hit " or ; early - break
            result = get_substr_till(pool[index+len(from_str):], break_chars)

    return result
def get_substr_from():
    pass

def get_substr_till(string, break_chars):
    result = ""
    for i in range(len(string)):
        if string[i] in break_chars:
            break
        result += string[i]
    return result
def get_left_margin(margins):
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

def remove_substr(string, substr):
    appending = False
    counter = 0
    result = ''
    for i in range(len(string)):
        if string[i:i+len(substr)] == substr:
            appending = False
            counter = len(substr)
        if not appending and counter == 0:
            appending = True
        if counter > 0:
            counter -= 1
        if appending:
            result += string[i]

    return result

def starts_with_link(par):
    if par[0:2] == "<A":
        return True
    else:
        return False
