# from oto import divider
from oto.importer import Importer

from oto.interpreter import Interpreter
from oto.exporter import Exporter
from oto.config import read_config


def main():
    config = read_config('./config')
    myImporter = Importer()

    # gets lines (p tags and other data) from each imported file
    # passes it to Interpreter to parse and change each line
    # and then to Exporter to print that line
    for imported_file in myImporter.get_files():
        Interpreter(imported_file)
        Exporter(imported_file, myImporter.export_filename)

    print("Success!")


if __name__ == "__main__":
    main()
