import argparse

from const import ARGS_PARSE_FILENAME_HELP, ARGS_PARSE_TEXT_HELP


def _get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'text', 
        nargs='?',
        help=ARGS_PARSE_TEXT_HELP,
    )
    parser.add_argument(
        '-f', '--filename',
        type=argparse.FileType('r'),
        dest='filename',
        help=ARGS_PARSE_FILENAME_HELP,
    )
    return parser


def load_text():
    parser = _get_argument_parser()
    args = parser.parse_args()

    text = ''
    if args.filename is not None:
        try:
            text = args.filename.read()
        except IOError:
            print "Could not find file {filename}".format(filename=args.filename)
            exit(1)
    elif args.text is not None:
        text = args.text
    else:
        parser.print_help()
        exit(0)

    return text
