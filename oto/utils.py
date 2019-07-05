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

