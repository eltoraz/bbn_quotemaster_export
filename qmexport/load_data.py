# import the data in CSV format, exported from MS Access
import csv

def qm_read(format='csv', filename=''):
    if format == 'csv':
        return import_csv(filename)

# read data in from CSV
def import_csv(filename):
    data = []
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append({a: row[a].strip() for a in row})

    return data
