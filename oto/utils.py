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
