"""Load data from a Quote Master-exported CSV file
"""
import csv

def import_data(format='csv', filename=''):
    """Return a list of dicts containing the data for the desired query;
    or `None` if the specified format is unsupported
    """
    if format == 'csv':
        return import_csv(filename)
    else:
        return None

def import_csv(filename):
    """Return a list of dicts containing the data read from the
    specified CSV file; the keys are the column headers
    """
    data = []
    with open(filename, encoding='iso8859_15') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append({a: row[a].strip() for a in row})

    return data
