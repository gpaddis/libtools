#!/usr/bin/env python3

import ntpath
import argparse
from sys import argv
from lxml import etree


def delete_if_exists(root, node):
    "Search for a node and delete it if exists."
    candidate = root.find(node)
    if candidate is not None:
        root.remove(candidate)
        print('Element {} was found and deleted.'.format(node))

def get_filename(path):
    "Get the filename only, no matter what the path is."
    head, tail = ntpath.split(path)
    filename = tail or ntpath.basename(head)
    return filename.split('.')[0]

def clean_gpr(input_file, output_file, report_name):
    "Clean the GPR file."
    # GPR files are encoded in Latin 1.
    with open(input_file, 'r', encoding="latin1") as f:
        read_data = f.read()

    # Trim all junk and keep the xml part only
    content = read_data.split('Parameter=|F|=XMLParameters/n')
    content = content[1].split('/n/n|F|=ChildFrameName/')
    xml_string = content[0].replace('/n', '')

    # Parse the xml with etree. I encode it in bytes to avoid
    # problems with the encoding declaration in the XML string.
    root = etree.XML(xml_string.encode('utf8'))

    # The text of <CrystalExportType> must be 'PDF'
    root.find('CrystalExportType').text = 'PDF'

    # Add <ReportFileName> element with text 'C:\Reports\{filename}.rpt'.
    report_file_name = etree.Element('ReportFileName')
    filename = report_name or get_filename(input_file)
    report_file_name.text = 'C:\\Reports\\' + filename + '.rpt'
    root.insert(0, report_file_name) # Insert the new node at the beginning

    # <OLAPSettings> must be removed if present.
    delete_if_exists(root, 'OLAPSettings')

    # <crDesignGUID> must be removed if present.
    delete_if_exists(root, 'crDesignGUID')

    # Save the prettyfied XML to the output file.
    xml_bytes = etree.tostring(root, pretty_print=True, encoding='utf8', xml_declaration=True)
    xml_string = xml_bytes.decode('utf8')
    out = output_file or 'Output.txt'
    with open(out, 'w') as f:
        f.write(xml_string)

    print("The output was saved in the file {}.".format(out))


if __name__ == '__main__':
    # Parse the arguments with argparse.
    parser = argparse.ArgumentParser(description="Extract the XML configuration from a GPR file.")
    parser.add_argument('input_file', help='The raw GPR file to process')
    parser.add_argument('-o', dest='output_file', required=False,
                        help='The output file name with extension (default: Output.txt)')
    parser.add_argument('-r', dest='report_name', required=False,
                        help='The <ReportFileName> without extension')
    args = parser.parse_args()

    clean_gpr(args.input_file, args.output_file, args.report_name)
