ocreror-detector
================

Runs some statistical analyses on text files to help spot errors in OCR.


Installation
------------

```
# git clone and cd to this repo
sudo apt-get install python python-pip python-virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Usage
-----

```
# cd to this repo
source venv/bin/activate
python ./find-bad-ocr.py <directory-of-text-files> <output-csv-file>
```

Metrics
-------
