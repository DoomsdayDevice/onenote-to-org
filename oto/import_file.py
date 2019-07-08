def import_file(filename):
    with open(filename, 'r') as fobj:
        return fobj.read()
