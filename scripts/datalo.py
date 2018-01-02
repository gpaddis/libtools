#!/usr/bin/env python

import csv
from sys import argv
import isbnlib

"""
Collect all identifiers from a csv file and output a list of unique
identifiers with an activation status for each one. The list will
be uploaded to the SFX Dataloader to mass update target portfolios.
"""

def extract_isbns(row):
    "Extract all canonical isbns from a row in the CSV file."
    all_isbns = []
    for field in row:
        isbns = isbnlib.get_isbnlike(field)
        for isbn in isbns:
            all_isbns.append(isbnlib.canonical(isbn))

    return list(set(all_isbns))  # Deduplicate the ISBNs

def collect_isbns(input_file):
    "Collect all ISBNs from the input file."
    reader = csv.reader(open(input_file, 'r')) # let the user define the delimiter
    collected_isbns = []
    for row in reader:
        collected_isbns += extract_isbns(row)

    return collected_isbns

def write_output(output_file, identifiers):
    "Write the list of identifiers to the output file."
    writer = csv.writer(open(output_file, "w"), dialect=csv.excel_tab)
    for identifier in identifiers:
        writer.writerow([identifier, 'ACTIVE']) # Get status from param


if __name__ == '__main__':
    identifiers = collect_isbns(argv[1]) # Use argparse instead!
    write_output(argv[2], identifiers)
