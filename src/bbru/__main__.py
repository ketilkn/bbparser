from argparse import ArgumentParser
from pprint import pprint as pp

from bbru.starplayer import parse_starplayer

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('infiles', nargs='+', type=str)

    args = parser.parse_args()

    for infile in args.infiles:
        with open(infile, 'r') as the_file:
            pp(parse_starplayer(the_file.read()), indent=2)
