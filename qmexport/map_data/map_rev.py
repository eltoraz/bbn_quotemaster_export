"""Process user-entered part revision data
"""
def map_rev(data):
    """Return a dict mapping part numbers to part revisions
    """
    rev_data = {}
    for entry in data:
        rev_data[entry['PartNum']] = entry['RevisionNum']

    return rev_data

def update_parts(part_data, rev_dict):
    """Update the part data with newly-entered revision numbers
    """
    count = 0
    for part in rev_dict:
        if part not in part_data:
            count += 1
            continue

        part_data[part].update({'RevisionNum': rev_dict[part],
                                'RevShortDesc': 'Revision ' + rev_dict[part]})
