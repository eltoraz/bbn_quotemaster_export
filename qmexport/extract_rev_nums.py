"""Extract revision numbers from prints (in PDF format)
for as many entries as possible
"""
import os
import re

import PyPDF2
from qmexport import config, load_data

def initialize():
    """Read in the data to prepare to extract the part revision
    numbers from PDFs
    """
    filename = config.qualified_filename('part')
    return load_data.qm_read(format='csv', filename=filename)

def extract_rev_num(page_content):
    """Return and extract the revision number from the text on
    the PDF print's first page
    """
    rev_num_regex = '[Rr]ev(?:\.?|ision):?\s*(\d{1,2})'

    regex_match = re.search(rev_num_regex, page_content)
    rev_num = regex_match.group(1) if regex_match else 'NULL'

    return rev_num

def parse_pdfs(part_rev_data):
    """Start the extraction process, loading the print paths from
    the CSV file, opening them, and reading off the text
    """
    revisions = {}
    for entry in part_rev_data:
        path_str = entry[config.print_path]
        if path and path_str != config.dummy_print:
            with open(os.path.normpath(path_str), 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                page_content = pdf_reader.getPage(0).extractText()

                rev_num = extract_rev_num(page_content)
        else:
            rev_num = ''

        revisions[entry[config.partnum]] = rev_num

    return revisions

def run_extraction():
    part_rev_data = initialize()
    revisions = parse_pdfs(part_rev_data)
