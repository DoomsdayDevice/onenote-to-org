from . import utils

def read_config(path):
    def import_config():
        with open(path, 'r') as fobj:
            return fobj.read()

    def find_block(text, block_name):
        """ returns start and end index of a block """

        block_start = utils.get_start(text, block_name)
        block_end = utils.get_index_of_next_char(text, block_start, '[') - 1

        return (block_start, block_end)

    def find_value(text, BS, BE, key):
        # finding source
        start = 0
        end = 0
        for i in range(BS, BE):
            if text[i:i+len(key)] == key:
                start = i+len(key)+2
                for j in range(start, BE):
                    if text[j] == '"':
                        end = j
                        break
                break
        return text[start:end]

    # find source location and attach to object
    block_name = "[converter]"
    text = import_config()
    block_start, block_end = find_block(text, block_name)

    import_file = find_value(text, block_start, block_end, "input")
    export_filename = find_value(text, block_start, block_end, "output")
