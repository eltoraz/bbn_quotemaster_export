# write converted data to CSV
import csv

def write_csv(fieldnames, data, filename):
    with open(filename, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)
