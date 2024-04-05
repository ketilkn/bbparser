from argparse import ArgumentParser
from pprint import pprint as pp

from bbru.inducements import parse_inducements
from bbru.starplayer import parse_starplayer
from bbru.teams import parse_team

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('import_type', choices=['starplayer', 'inducement', 'team'], nargs='?', default='starplayer', type=str)
    parser.add_argument('infiles', nargs='+', type=str)

    args = parser.parse_args()

    for infile in args.infiles:
        with open(infile, 'r') as the_file:
            if args.import_type == 'inducement':
                for inducement in parse_inducements(the_file.read()):
                    #pp(inducement, indent=2)
                    print(inducement['title'])
                    print(inducement['description'])
                    print('======')
            elif args.import_type == 'team':
                pp(parse_team(the_file.read()), indent=2)
            else:
                pp(parse_starplayer(the_file.read()), indent=2)
