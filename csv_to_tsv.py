#!/usr/bin/env python

import os
import sys
import csv

"""
This script is adapted from:
https://github.com/realpython/python-scripts/blob/master/scripts/19_tsv-to-csv.py
"""


def convert(input, out):
    if os.path.exists(out):
        raise ValueError("Output file already exists")

    reader = csv.reader(open(input, 'rU'), dialect="excel")
    writer = csv.writer(open(out, "wb+"), dialect=csv.excel_tab)
    for row in reader:
        writer.writerow(row)


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
