#!/usr/bin/env python

import sys
PY3 = sys.version_info > (3,)
import re
import csv
import os
if PY3:
    from queue import Queue
else:
    from Queue import Queue
from threading import Thread
from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA, SimpleProgress

DEBUG = False
# DEBUG = True
NUM_WORKERS = 30
MAX_FILES = -1
FIELD_NAMES = ['avg_word_length', 'avg_words_per_line', 'nr_lines', 'nr_different_words', 'nr_unique_words', 'has_consecutive_pagebreaks', 'id']

def _re_matches(regex, line):
    m = re.search(regex, line)
    return m == None

def is_numeric(line):
    return re.match('^[0-9\.,]+$', line.strip())

def has_pagebreak(line):
    return _re_matches('\x0c+', line)

def has_consecutive_pagebreaks(line):
    return _re_matches('\x0c{2,}', line)

def avg(vals):
    if len(vals) == 0:
        return 0
    return float(sum(vals)) / len(vals)

def analyze_worker(q, bar, csv_writer, files):
    while not q.empty():
        fileIdx = q.get()
        filename = files[fileIdx]
        basename = os.path.basename(filename)
        report = analyze_file(filename)
        report['id'] = basename
        csv_writer.writerow(report)
        q.task_done()
        bar.next()

def analyze_file(filename):
    with open(filename, 'r') as f:
        report = {}
        avg_word_lengths = []
        avg_words_per_line = []
        nr_lines = 0
        word_histogram = {}
        for line in f:
            word_lengths = []
            report['has_consecutive_pagebreaks'] = has_consecutive_pagebreaks(line)
            words = line.split('\x20')
            words_per_line = len(words)
            if words_per_line <= 1:
                continue
            nr_lines += 1
            avg_words_per_line.append(words_per_line)
            for word in words:
                if is_numeric(word):
                    continue
                if word in word_histogram:
                    word_histogram[word] += 1
                else:
                    word_histogram[word] = 1
                word_lengths.append(len(word))
            avg_word_lengths.append(avg(word_lengths))
        report['avg_word_length'] = avg(avg_word_lengths)
        report['avg_words_per_line'] = avg(avg_words_per_line)
        report['nr_lines'] = nr_lines
        report['nr_different_words'] = len(word_histogram)
        report['nr_unique_words'] = len([w for w in word_histogram if word_histogram[w] == 1])
        return report

if __name__ == '__main__':
    if DEBUG:
        txtpath = 'as-text'
        outfile = 'ocr-analysis.csv'
        MAX_FILES = 200
    else:
        try:
            txtpath = sys.argv[1]
            outfile = sys.argv[2]
        except IndexError:
            print("Usage: %s <directory-of-text-files> <output-csv-file>" % sys.argv[0])
            sys.exit(1)

    print("Queuing files")
    q = Queue()
    files = []
    idx = 0
    for basename in os.listdir(txtpath):
        filename = os.path.join(txtpath, basename)
        if MAX_FILES > -1 and idx >= MAX_FILES:
            break
        if os.path.isfile(filename):
            files.append(filename)
            q.put(idx)
            idx += 1

    widgets = ['Analyzing: ', Percentage(), ' ', SimpleProgress(), ' ', Bar('#'), ' ', ETA()]
    bar = ProgressBar(widgets=widgets)(files)

    if PY3:
        f = open(outfile, 'wt', encoding='utf8', newline='')
    else:
        f = open(outfile, 'wb', 0)
    csv_writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
    csv_writer.writeheader()
    print("Starting threads (#%s)" % NUM_WORKERS)
    for i in range(NUM_WORKERS):
        t = Thread(target=analyze_worker, args=[q, bar, csv_writer, files])
        t.daemon = True
        t.start()
    q.join()
    bar.finish()

