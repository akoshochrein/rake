from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rake',
    version='0.0.3',
    description='The RAKE keyword extraction algorithm in Pyhton',
    long_description=long_description,
    url='https://github.com/akoskaaa/rake',
    author='Akos Hochrein',
    author_email='hoch.akos@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'scripts']),
    install_requires=[
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'prake=src:run',
        ],
    },
)
