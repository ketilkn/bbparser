from pprint import pprint as pp

import argparse

from dadidimerda.inducements import parse_inducements

if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('infile', type=str)

    arguments = argparse.parse_args()

    with open(arguments.infile, 'r') as in_file:
        txt = in_file.read()
        inducements = list(parse_inducements(txt))

        pp(inducements, indent=2)
