#!/usr/bin/env python3

import csv
import argparse
from sys import argv
import lib.identifiers as ids

"""
This script compares two lists of eBooks. The ISBNs found in the first list
are compared against the ones found in the second list. The titles present
in both files are saved in the file matches.csv, while the ones not found
in the second list are saved in the file missing.csv.

The script accepts and produces tab delimited files.
"""

def compare_lists(first_csv, second_csv):
    "Compare two CSV files for matching & missing eBook titles."
    isbns_to_compare = []

    # Create a list of ISBNs from the second file.
    with open(second_csv, 'r', encoding="utf-8") as input_csv:
        data_reader = csv.reader(input_csv)
        for row in data_reader:
            isbns_to_compare += ids.extract_isbns(row)

    # Open the first CSV and check the ISBNS one by one
    with open(first_csv, 'r', encoding="utf-8") as input_csv:
        data_reader = csv.reader(input_csv, dialect='excel-tab')
        header = next(data_reader)

        matches = [header]
        matches_count = 0

        missing = [header]
        missing_count = 0

        for row in data_reader:
            isbns = ids.extract_isbns(row)

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
    with open("matches.csv", 'w', encoding="utf-8", newline='') as output_csv:
        writer = csv.writer(output_csv, dialect='excel-tab')
        writer.writerows(matches)

    print("However, {} titles are missing from the second list. I saved these in missing.csv.".format(missing_count))
    with open("missing.csv", 'w', encoding="utf-8", newline='') as output_csv:
        writer = csv.writer(output_csv, dialect='excel-tab')
        writer.writerows(missing)


if __name__ == '__main__':
    # Parse the arguments with argparse.
    parser = argparse.ArgumentParser(description="Compare two CSV files for matching & missing eBook titles.")
    parser.add_argument('first_csv', help='The first eBook title list')
    parser.add_argument('second_csv', help='The second eBook title list')
    args = parser.parse_args()

    compare_lists(args.first_csv, args.second_csv)
