import sys

from .core import rake
from .loader import load_text


def run():
    text = load_text()
    keywords_with_rank = rake(text)
    for pair in sorted(list(keywords_with_rank.items()), key=lambda e: (e[0], e[1]), reverse=True)[:len(keywords_with_rank)//3]:
        sys.stdout.write('{rank}\t{keyword}\n'.format(
            keyword=pair[0],
            rank=pair[1],
        ))
