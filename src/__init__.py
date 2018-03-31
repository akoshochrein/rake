import argparse
import re

from collections import defaultdict

from const import (
    ARGS_PARSE_FILENAME_HELP, ARGS_PARSE_TEXT_HELP, COMMON_STOP_WORDS, PADDED_COMMON_STOP_WORDS,
    PUNCTUATION,
)


word_regex_map = {
    word: {
        'prefix': re.compile('^' + word + ' '),
        'suffix': re.compile(' ' + word + '$')
    } for word in COMMON_STOP_WORDS
}

punctuation_regex_map = {
    punctuation: re.compile(punctuation.strip()) for punctuation in PUNCTUATION
}


def get_candidates(text):
    separator_regex = '|'.join(PUNCTUATION + PADDED_COMMON_STOP_WORDS)

    # zero tier candidates get just separated by punctuation and common stop words
    candidates = re.split(separator_regex, text)
    candidates = [candidate.lower() for candidate in candidates]

    # first tier candidates have stuck common stop words removed from them
    stripped_candidates = []
    for candidate in candidates:
        new_candidate = candidate
        while True:
            for word in COMMON_STOP_WORDS:
                new_candidate = re.sub(word_regex_map[word]['prefix'], '', new_candidate, re.IGNORECASE)
                new_candidate = re.sub(word_regex_map[word]['suffix'], '', new_candidate, re.IGNORECASE)
            if new_candidate == candidate:
                break
            candidate = new_candidate
        stripped_candidates.append(new_candidate)

    # second tier candidates should not include common stop words
    filtered_candidates = [
        candidate for candidate in stripped_candidates if candidate not in COMMON_STOP_WORDS
    ]

    # third tier candidates get cleaned up from punctuation
    cleaned_candidates = []
    for candidate in filtered_candidates:
        for punctuation in PUNCTUATION:
            candidate = re.sub(punctuation_regex_map[punctuation], '', candidate)
        cleaned_candidates.append(candidate)

    return cleaned_candidates


def get_keyword_matrix(candidates):
    keyword_matrix = defaultdict(list)
    for candidate in candidates:
        words = candidate.split(' ')
        for word in words:
            keyword_matrix[word] += words

    deg_freq_by_keyword = {
        keyword: {
            'freq': len(vertices),
            'deg': vertices.count(keyword)
        } for keyword, vertices in keyword_matrix.items()
    }

    return deg_freq_by_keyword


def get_keywords_with_rank(candidates, keyword_matrix):
    candidate_matrix = {candidate: {'deg': 0, 'freq': 0} for candidate in candidates}
    for keyword, value in keyword_matrix.items():
        for candidate in candidate_matrix.keys():
            if keyword in candidate:
                candidate_matrix[candidate]['deg'] += value['deg']
                candidate_matrix[candidate]['freq'] += value['freq']

    return {
        key: value['freq'] / float(value['deg']) for key, value in candidate_matrix.items()
    }


def run():
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

    candidates = get_candidates(text.strip())
    keyword_matrix = get_keyword_matrix(candidates)
    keywords_with_rank = get_keywords_with_rank(candidates, keyword_matrix)
    print sorted(keywords_with_rank.items(), key=lambda (k, v): (v, k), reverse=True)[:len(candidates)//3]
