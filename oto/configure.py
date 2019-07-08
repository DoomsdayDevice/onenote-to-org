import argparse
import glob

def parse_args():
    """ returns tuple with input and output """
    parser = argparse.ArgumentParser(description="Convert Onenote HTML to Org-mode")
    parser.add_argument('input', metavar='I', type=str, nargs=1,
                        help='Input file or folder name')
    parser.add_argument('output', metavar='O', type=str, nargs=1,
                        help='Output folder name')

    parser.add_argument('--divide', dest='divide', action='store_const',
                        const=sum, default=max,
                        help="""Divide the imported onenote files into sub-pages.
                             Use when you import an entire notebook""")

    args = parser.parse_args()

    return (args.input[0], args.output[0])

def parse_config():
    pass

def parse_input(pattern):
    print("THE GLOBS:", glob.glob(pattern))
    return glob.glob(pattern)

def configure():
    config = {}
    config['input'], config['output'] = parse_args()
    print("--------------------------------------------")
    config['list_of_files'] = parse_input(config['input'])

    # config[''] = parse_config()

    return config
