# qmexport.py - module for migrating BBN data generated by Quote Master
#  to CSV format usable by Epicor ERP's DMT
from qmexport import config, load_data, write_data

from qmexport.part import Part
from qmexport.material import Material
from qmexport.operation import Operation

from qmexport.map_data import map_part, map_bom, map_boo

# TODO: revision dict

# get the data
# for now, by opening a CSV of the result set of the queries
part_filename = config.qualified_filename('part')
bom_filename = config.qualified_filename('bill of materials')
boo_filename = config.qualified_filename('bill of operations')

part_data = load_data.qm_read(format='csv', filename=part_filename)
bom_data = load_data.qm_read(format='csv', filename=bom_filename)
boo_data = load_data.qm_read('csv', boo_filename)

# map QM values to fields expected by DMT, scrubbing & 
#  reformatting as necessary
dmt_part_data = map_part.map_part(part_data)
dmt_bom_data = map_bom.map_bom(bom_data, rev_dict)
dmt_boo_data = map_boo.map_boo(bom_data, rev_dict)

# export the Epicor-friendly data
write_data.write_csv(Part.expected_fields,
                     dmt_part_data,
                     config.output_path+'part_ALL.csv')

write_data.write_csv(config.part_header.split(','),
                     dmt_part_data,
                     config.output_path+'part.csv')
write_data.write_csv(config.part_plant_header.split(','),
                     dmt_part_data,
                     config.output_path+'part_plant.csv')
write_data.write_csv(config.part_rev_header.split(','),
                     dmt_part_data,
                     config.output_path+'part_rev.csv')


# --- DEBUGGING ---
print('---PART---')
print(len(part_data))
print(part_data[0])

print('---PART (DMT)---')
print(len(dmt_part_data))
first = dmt_part_data[part_data[0][config.partnum]]
print(first)

print('')

'''
counts = {}
for i in dmt_part_data:
    counts[i['ClassID']] = counts.get(i['ClassID'], 0) + 1
print('ClassID breakdown:', counts)

asbl_counts = {'1': 0, '0': 0}
for i in part_data:
    asbl_counts[i['NRCCPrint']] += 1
print('Assembly count:', asbl_counts)
'''
