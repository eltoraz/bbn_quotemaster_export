# crawler.py - crawl the directory structure housing the Inventor files
#  to parse revision numbers from the filenames
import os
import re
import string

def _get_revs(path):
    """Return a dict mapping drawing numbers to the associated revision
    number for items in the given directory.

    Ignore subdirectories, and files with the same name but different
    extension, and Inventor drawings without a revision suffix
    """
    working_dict = {}
    file_regex = '([A-Za-z]{3}-\d{3})-(\w{1,2})'

    for entry in os.listdir(path):
        file_match = re.match(file_regex, entry)
        full_filename = os.path.abspath(os.path.join(path, entry))
        if os.path.isfile(full_filename) and file_match:
            working_dict[file_match.group(1) = file_match.group(2)]

    return working_dict

def run():
    """Return a dict mapping drawing numbers to revision numbers for all
    parts with an Inventor document in the design/development path
    """
    rev_nums = {}
    path = 'I:/Cadd/'

    for subdir in string.ascii_uppercase:
        rev_nums.update(_get_revs(os.path.abspath(path + subdir + '/')))

    return rev_nums
