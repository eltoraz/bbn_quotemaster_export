"""Extract revision numbers from prints (in PDF format)
for as many entries as possible
"""
import os
import re

import PyPDF2
from qmexport import config, load_data

def extract_rev_num(page_content):
    """Return and extract the revision number from the text on
    the PDF print's first page
    """
    rev_num = '01'
    rev_num_regex = '[Rr]ev(?:\.?|ision):?\s*(\w{2})'

    return rev_num

def start_extraction():
    """Start the extraction process, loading the print paths from
    the CSV file, opening them, and reading off the text
    """
    part_rev_filename = config.qualified_filename('part revision')
    part_rev_data = load_data.qm_read(format='csv', filename=part_rev_filename)

    for entry in part_rev_data:
        path_str = entry['Image_Path']
        if path_str != config.dummy_print:
            with open(os.path.normpath(path_str), 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                page_content = pdf_reader.getPage(0).extractText()

                rev_num = extract_rev_num(page_content)
        else:
            rev_num = 'NULL'
