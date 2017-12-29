#!/usr/bin/env python

import csv
import isbnlib
from sys import argv

"""
This script compares two lists of eBooks. The ISBNs found in the first list
are compared against the ones found in the second list. The titles present
in both files are saved in the file matches.csv, while the ones not found
in the second list are saved in the file missing.csv.

The script accepts and produces tab delimited files.
"""

def get_isbns(row):
    "Collect all canonical isbns from a row in the CSV file."
    all_isbns = []
    for field in row:
        isbns = isbnlib.get_isbnlike(field)
        for isbn in isbns:
            all_isbns.append(isbnlib.canonical(isbn))

    return list(set(all_isbns)) # Deduplicate the ISBNs

def compare_lists(first_csv, second_csv):
    "Compare two CSV files for matching & missing eBook titles."
    isbns_to_compare = []

    # Create a list of ISBNs from the second file.
    with open(second_csv, 'r') as input_csv:
        data_reader = csv.reader(input_csv)
        for row in data_reader:
            isbns_to_compare += get_isbns(row)

    # Open the first CSV and check the ISBNS one by one
    with open(first_csv) as input_csv:
        data_reader = csv.reader(input_csv, dialect='excel-tab')
        header = data_reader.next()

        matches = [header]
        matches_count = 0

        missing = [header]
        missing_count = 0

        for row in data_reader:
            isbns = get_isbns(row)

            found = False
            for isbn in isbns:
                if isbn in isbns_to_compare:
                    found = True

            if found == True:
                matches.append(row)
                matches_count += 1
            else:
                missing.append(row)
                missing_count += 1

    print("I have found {} titles in the second list and saved them in matches.csv.".format(matches_count))
    with open("matches.csv", 'wb+') as output_csv:
        writer = csv.writer(output_csv, dialect='excel-tab')
        writer.writerows(matches)

    print("However, {} titles are missing from the second list. I saved these in missing.csv.".format(missing_count))
    with open("missing.csv", 'wb+') as output_csv:
        writer = csv.writer(output_csv, dialect='excel-tab')
        writer.writerows(missing)


if __name__ == '__main__':
    script, first_csv, second_csv = argv
    compare_lists(first_csv, second_csv)
