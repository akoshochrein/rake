# pRAKE

[pRAKE](https://github.com/akoskaaa/rake) is an implementation of the [RAKE](https://www.researchgate.net/publication/227988510_Automatic_Keyword_Extraction_from_Individual_Documents) algorithm in Python. The goal of the project is to give a reliadble and fast keyword extraction algorithm for everyone.

## Installation

pRAKE wil require pip to be installed. If you don't have pip, look for installation pointers [here](https://pip.pypa.io/en/stable/installing/).

```sh
pip install prake
```

## Usage

The command for using pRAKE is `prake`. Without any arguments, the command prints usage information.
```sh
prake
usage: prake [-h] [-f FILENAME] [text]

positional arguments:
  text                  Text for the RAKE algorithm to be ran against.

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        The desired filename for the RAKE algorithm to execute
                        against.
```

The following commands are equivalent:
```sh
prake <contents of textfile-to-analyze.txt>
prake -f textfile-to-analyze.txt
prake --filename textfile-to-analyze.txt
cat textfile-to-analyze.txt | prake
```

## Development
Pull requests and issues are always welcome. If you want to work on something, please open an issue for it first and send a pull request.

### Testing
pRAKE currently runs under Python 2.7 and we are running tests under the same environment using `tox` and `pytest`. If you make some modifications, please indicate that change in the form of a test as well.
