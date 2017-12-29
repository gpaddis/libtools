#!/usr/bin/env python3

import ntpath
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

def clean_gpr(input_file):
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
    filename = get_filename(input_file)
    report_file_name.text = 'C:\\Reports\\' + filename + '.rpt'
    root.insert(0, report_file_name) # Insert the new node at the beginning

    # <OLAPSettings> must be removed if present.
    delete_if_exists(root, 'OLAPSettings')

    # <crDesignGUID> must be removed if present.
    delete_if_exists(root, 'crDesignGUID')

    # Save the prettyfied XML to the output file.
    xml_bytes = etree.tostring(root, pretty_print=True, encoding='utf8', xml_declaration=True)
    with open('Output.txt', 'wb') as f:
        f.write(xml_bytes)

    print("The output was saved in the file Output.txt.")

if __name__ == '__main__':
    clean_gpr(argv[1])
