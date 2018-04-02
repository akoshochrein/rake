import re

from collections import defaultdict

from .const import COMMON_STOP_WORDS, PADDED_COMMON_STOP_WORDS, PUNCTUATION


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
        key: value['freq'] / float(value['deg']) for key, value in list(candidate_matrix.items())
    }


def rake(text):
    candidates = get_candidates(text.strip())
    keyword_matrix = get_keyword_matrix(candidates)
    return get_keywords_with_rank(candidates, keyword_matrix)
