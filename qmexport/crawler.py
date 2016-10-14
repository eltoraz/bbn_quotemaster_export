# crawler.py - crawl the directory structure housing the Inventor files
#  to parse revision numbers from the filenames
import os
import re
import string

from qmexport import config, load_data

def _check_canonical(working_dict, draw_num, new_rev):
    """Return True if the new revision number should be stored in the dict
    (possibly overwriting previous value) based on the following criteria:
    - specified `draw num` has not entry in the `working_dict` yet
    - both are same type (both numerical or both alph) and new > old, OR
    - new is numerical and old is strictly alph

    Return False otherwise
    """
    if draw_num not in working_dict:
        return True

    num_regex = '\d{1,2}-\d{1,2}'
    chr_regex = '[A-Za-z]{1,2}-[A-Za-z]{1,2}'

    old_rev = working_dict[draw_num]
    joined_revs = '-'.join([old_rev, new_rev])

    if re.match(num_regex, joined_revs) or re.match(chr_regex, joined_revs):
        if new_rev > old_rev:
            return True
    elif re.match('\d{1,2}', new_rev):
        # if they're not the same format, but the new is numerical, keep it
        return True

    return False

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
            draw_num = file_match.group(1)
            revn_num = file_match.group(2)
            # need to check whether to overwrite existing rev num
            if _check_canonical(working_dict, draw_num, revn_num):
                working_dict[draw_num] = revn_num

    return working_dict

def _get_qm_data():
    """Return a dict mapping drawing numbers to a list of part numbers
    each corresponds to, using data read in from a Quote Master query
    """
    # read in data
    proc_data_filename = config.qualified_filename('process plan')
    proc_data = load_data.import_data('csv', proc_data_filename)

    draw_num_re = '([a-zA-Z]{3}-\d{3})'
    drawnum_part_map = {}
    for entry in proc_data:
        working_dn = entry[config.drawnum]
        working_pn = entry[config.partnum]

        # discard entries with non-standard process plans
        # (they won't match any of the items the crawler finds anyway)
        if not re.match(draw_num_re, working_dn):
            continue

        if working_dn in drawnum_part_map:
            drawnum_part_map[working_dn].append(working_pn)
        else:
            drawnum_part_map[working_dn] = [working_pn]

    return drawnum_part_map

def run():
    """Return a dict mapping part numbers to revision numbers for all
    parts with an Inventor document in the design/development workspace
    """
    drawnum_rev_map = {}
    path = 'I:/Cadd/'

    for subdir in string.ascii_uppercase:
        drawnum_rev_map.update(_get_revs(os.path.abspath(path + subdir + '/')))

    drawnum_part_map = _get_qm_data()

    partnum_rev_map = {}
    for dn in drawnum_rev_map:
        for pn in drawnum_part_map.get(dn, []):
            partnum_rev_map[pn] = drawnum_rev_map[dn]

    return partnum_rev_map
