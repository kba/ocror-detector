ocreror-detector
================

Runs some statistical analyses on text files to help spot errors in OCR.


Installation
------------

```
# git clone and cd to this repo
sudo apt-get install python python-pip python-virtualenv
# for Python3: sudo apt-get install python3 python3-pip python3-virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
# for Python3: pip3 install -r requirements.txt
```

Usage
-----

```
# cd to this repo
source venv/bin/activate
./find-bad-ocr.py <directory-of-text-files> <output-csv-file>
```

Troubleshooting
---------------

`ImportError: No module named 'progressbar'`

Make sure the python version used in the `virtualenv` call matches
`/usr/bin/env python` or invoke the python interpreter directly, i.e.
`python3 find-bad-ocr.py` or `python2 find-bar-ocr.py`.

Metrics
-------

## avg_word_length

The arithmetic mean of the arithmetic mean word length per lines.

## avg_words_per_line

The arithmetic mean of the number of non-numeric per line.

## nr_lines

The number of lines in the file.

## nr_different_words

The number of different words in the text

## nr_unique_words

The number of words that appear only once

## has_consecutive_pagebreaks

Whether the file contains multiple consecutive pagebreaks (`^L`, `\x0c`, ascii 12)

## nr_words 

Total number of words
