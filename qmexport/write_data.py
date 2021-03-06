"""write data converted from Quote Master to Epicor-compatible
format to a CSV for use with Epicor DMT
"""
import csv
import os

def write_csv(fieldnames, data, filename):
    """Write a CSV file at `filename` with headers (and order)
    specified by `fieldnames` and body in `data` (a list of dicts
    with keys matching the fields)
    """
    # create the output directory if it doesn't already exist
    if not os.path.isdir(os.path.dirname(filename)):
        os.mkdirs(os.path.dirname(filename))

    with open(filename, 'w', encoding='iso8859_15') as csv_file:
        csv_writer = csv.DictWriter(csv_file,
                                    extrasaction='ignore',
                                    fieldnames=fieldnames,
                                    lineterminator='\n')
        csv_writer.writeheader()
        if isinstance(data, dict):
            csv_writer.writerows([row.__dict__ for row in data.values()])
        else:
            # passed a straight-up list of rows
            csv_writer.writerows([row.__dict__ for row in data])
