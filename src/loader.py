import argparse
import sys

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
        text = args.filename.read()
    elif args.text is not None:
        text = args.text
    elif not sys.stdin.isatty():
        for line in sys.stdin:
            text += line

    if not text:
        parser.print_help()
        exit(0)

    return text
