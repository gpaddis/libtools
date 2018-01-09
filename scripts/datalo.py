#!/usr/bin/env python

import csv
import argparse
from sys import argv
import lib.identifiers as ids

"""
Collect all identifiers from a csv file and output a list of unique
identifiers with an activation status for each one. The list will
be uploaded to the SFX Dataloader to mass update target portfolios.
"""

def collect_isbns(input_file):
    "Collect all ISBNs from the input file."
    reader = csv.reader(open(input_file, 'r', encoding="utf-8")) # let the user define the delimiter
    collected_isbns = []
    for row in reader:
        collected_isbns += ids.extract_isbns(row)

    return collected_isbns

def write_output(output_file, identifiers, flag):
    "Write the list of identifiers to the output file."
    writer = csv.writer(open(output_file, "w"), dialect=csv.excel_tab)
    for identifier in identifiers:
        writer.writerow([identifier, flag]) # Get status from param


if __name__ == '__main__':
    # Parse the arguments with argparse.
    parser = argparse.ArgumentParser(
        description="Extract all identifiers from a CSV file and prepare a list for the SFX dataloader.")
    parser.add_argument('input_file', help='The CSV file to process')
    parser.add_argument('output_file', help='The TSV file for the dataloader')
    parser.add_argument('-f', dest='flag', required=False, default="ACTIVE",
                        help='The flag for each entry (default: "ACTIVE")')
    args = parser.parse_args()

    identifiers = collect_isbns(args.input_file)
    write_output(args.output_file, identifiers, args.flag)
