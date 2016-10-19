# qmexport.py - module for migrating BBN data generated by Quote Master
#  to CSV format usable by Epicor ERP's DMT
import os
import math

from qmexport import config, crawler, dmt, load_data, log, write_data

from qmexport.part import Part
from qmexport.material import Material
from qmexport.operation import Operation

from qmexport.map_data import map_part, map_bom, map_boo, map_rev

def debug(test_single_pn):
    """Print info about the data structures for debugging
    """
    print('---PART---')
    print(len(part_data), 'raw part entries')
    #print(part_data[0])

    print('---PART (DMT)---')
    print(len(dmt_part_data), 'processed part entries')
    #print(dmt_part_data[test_single_pn])

    def _missing_req_rev(pn):
        """Return True if the part specified is missing a revision number
        and is present in a BOO/BOM (and thus requires one); False otherwise
        """
        return (pn in dmt_bom_data or pn in dmt_boo_data) and (not dmt_part_data[pn].RevisionNum)

    print('---PARTS MISSING REVISION NUMBERS---')
    missing_revs = [pn for pn in dmt_part_data.keys() if _missing_req_rev(pn)]
    missing_rev_parts = [dmt_part_data[part] for part in missing_revs]
    print(len(missing_revs), 'parts need revision numbers manually specified')
    write_data.write_csv(config.part_rev_header.split(','),
                         missing_rev_parts,
                         config.output_path+'missing_part_revs.csv')

    print('---BOM---')
    print(len(bom_data), 'BOM entries read in')
    print(len(dmt_bom_data), 'unique parts with BOM entries')
    #print(dmt_bom_data[test_single_pn])

    print('---BOO---')
    print(len(boo_data), 'BOO entries read in')
    print(len(dmt_boo_data), 'unique parts with BOO entries')
    #print(dmt_boo_data[test_single_pn])

    print('---UNMAPPED CLASSKEYS---')
    unmapped_classkeys = set()
    for row in dmt_part_data:
        classid = dmt_part_data[row].__dict__['ClassID']
        if classid[0] == '!':
            unmapped_classkeys = set.union(unmapped_classkeys, {classid[1:-1]})
    print(len(unmapped_classkeys), 'classkeys not mapped to Epicor values:')
    print(unmapped_classkeys)

    print('---UNMAPPED OPERATIONS---')
    missing_ops = set()
    for row in boo_data:
        if row[config.op_code] not in config.operation_mapping:
            missing_ops = set.union(missing_ops, {row[config.op_code]})
    print(len(missing_ops), 'operations not mapped to Epicor values:')
    print(missing_ops)

    print('---MISSING PARTS REFERENCED IN BOM---')
    missing_parts = set()
    for row in dmt_bom_data:
        for mat in dmt_bom_data[row]:
            pn = mat.__dict__['PartNum']
            mn = mat.__dict__['MtlPartNum']
            if pn not in dmt_part_data:
                missing_parts = set.union(missing_parts, {pn})
            if mn not in dmt_part_data:
                missing_parts = set.union(missing_parts, {mn})
    print(len(missing_parts), 'orphaned parts:')
    print(missing_parts)

    print('---PARTS MISSING EITHER A BOM OR BOO---')
    bom_keys = set(dmt_bom_data.keys())
    boo_keys = set(dmt_boo_data.keys())
    print('parts with a BOM but not BOO:', bom_keys - boo_keys)
    print('parts with a BOO but not BOM:', boo_keys - bom_keys)

def resolve_bom(data, pn):
    """Recurse over the rows in `data` belonging to part `pn` and
    return a list containing all its dependent materials
    """
    header = 'MtlPartNum'
    if pn in data:
        master_list = data[pn]
        working_list = []
        for row in master_list:
            working_list += resolve_bom(data, row.__dict__[header])
        return master_list + working_list
    else:
        return []

def resolve_boo(data, bom):
    """Return a list of Operation objects corresponding to the hierarchy
    of materials in the given BOM
    """
    working_list = []
    for row in bom:
        pn = row.__dict__['PartNum']
        if pn in data:
            working_list += data[pn]

    return working_list

def resolve_part_list(data, bom):
    """Return a dict of part numbers to Part objects for the given
    Bill of Materials (input as a list of Material objects); and
    a set of parts not in the part list
    """
    working_part_list = {}
    for mat in bom:
        pn = mat.__dict__['PartNum']
        mn = mat.__dict__['MtlPartNum']
        working_part_list[pn] = data[pn]
        working_part_list[mn] = data[mn]

    return working_part_list

def dmt_test(test_single_pn, test_complex_pn):
    """Generate short CSV files to test program output with DMT
    """
    # single-layer part w/ associated BOM & BOO
    log.log('Running small-scale data set & DMT tests...')
    test_single_bom = resolve_bom(dmt_bom_data, test_single_pn)
    test_single_boo = resolve_boo(dmt_boo_data, test_single_bom)

    test_single_part_list = resolve_part_list(dmt_part_data, test_single_bom)

    write_data.write_csv(Part.expected_fields,
                         test_single_part_list,
                         config.output_path+'TEST_Apart_ALL.csv')
    write_data.write_csv(config.part_header.split(','),
                         test_single_part_list,
                         config.output_path+'TEST_1part.csv')
    write_data.write_csv(config.part_plant_header.split(','),
                         test_single_part_list,
                         config.output_path+'TEST_2part_plant.csv')
    write_data.write_csv(config.part_rev_header.split(','),
                         test_single_part_list,
                         config.output_path+'TEST_3part_rev.csv')
    write_data.write_csv(Material.expected_fields,
                         test_single_bom,
                         config.output_path+'TEST_4bom.csv')
    write_data.write_csv(Operation.expected_fields,
                         test_single_boo,
                         config.output_path+'TEST_5boo.csv')

    # multi-layer part w/ associated BOM & BOO
    test_complex_bom = resolve_bom(dmt_bom_data, test_complex_pn)
    test_complex_boo = resolve_boo(dmt_boo_data, test_complex_bom)
    test_complex_part_list = resolve_part_list(dmt_part_data, test_complex_bom)

    # use dummy values for classids that haven't been mapped yet
    for part in test_complex_part_list:
        if test_complex_part_list[part].ClassID[0] == '!':
            test_complex_part_list[part].ClassID = 'OTHR'

    write_data.write_csv(Part.expected_fields,
                         test_complex_part_list,
                         config.output_path+'TEST_Bpart_ALL.csv')
    write_data.write_csv(config.part_header.split(','),
                         test_complex_part_list,
                         dmt.output_filename('Part', True, 1))
    write_data.write_csv(config.part_plant_header.split(','),
                         test_complex_part_list,
                         dmt.output_filename('Part Plant', True, 1))
    write_data.write_csv(config.part_rev_header.split(','),
                         test_complex_part_list,
                         dmt.output_filename('Part Revision', True, 1))
    write_data.write_csv(Material.expected_fields,
                         test_complex_bom,
                         dmt.output_filename('Bill of Materials', True, 1))
    write_data.write_csv(Operation.expected_fields,
                         test_complex_boo,
                         dmt.output_filename('Bill of Operations', True, 1))

    # run the DMT on the example files, with debug=True to limit the test
    log.log('Calling DMT on test data...')
    test_seg = {'part': 1, 'bom': 1, 'boo': 1}
    dmt.run_all(test_seg, True)

# get the data
# for now, by opening a CSV of the result set of the queries
part_filename = config.qualified_filename('part')
bom_filename = config.qualified_filename('bill of materials')
boo_filename = config.qualified_filename('bill of operations')

log.log('Reading in Quote Master data...')
part_data = load_data.import_data('csv', part_filename)
bom_data = load_data.import_data('csv', bom_filename)
boo_data = load_data.import_data('csv', boo_filename)

# map QM values to fields expected by DMT, scrubbing & 
#  reformatting as necessary
dmt_part_data = map_part.map_part(part_data)

# import part revisions (if they exist) for use in BOM/BOO
log.log('Crawling design/development folder for part revision numbers...')
part_rev_filename = config.qualified_filename('part revision')
rev_dict = crawler.run()
#if os.path.isfile(part_rev_filename):
#    rev_data = load_data.import_data('csv', part_rev_filename)
#    rev_dict = map_rev.map_rev(rev_data)
map_rev.update_parts(dmt_part_data, rev_dict)

log.log('Converting data to Epicor format...')
dmt_bom_data = map_bom.map_bom(bom_data, rev_dict)
dmt_boo_data = map_boo.map_boo(boo_data, rev_dict)

# only parts that appear in a BOM or BOO strictly need revision numbers
rev_subset = list(dmt_bom_data.keys())
rev_subset.extend([i for i in dmt_boo_data.keys() if i not in rev_subset])
dmt_part_rev_data = {part: dmt_part_data[part] for part in rev_subset}

# split data into groups of 1000 records
split = 1000
seg_count = {'part': math.ceil(len(dmt_part_data)/split),
             'bom': math.ceil(len(bom_data)/split),
             'boo': math.ceil(len(boo_data)/split)}

# export the Epicor-friendly data
log.log('Writing converted data to CSVs in ' + config.output_path)
write_data.write_csv(Part.expected_fields,
                     dmt_part_data,
                     config.output_path+'part_ALL.csv')

# above, replace `dmt_part_rev_data` with `dmt_part_data` if revision numbers
# are needed for all parts
part_rows = [dmt_part_data[key] for key in dmt_part_data]
for i in range(seg_count['part']):
    offset = i * split
    app_str = '{0}'.format(i+1)
    write_data.write_csv(config.part_header.split(','),
                         part_rows[offset:offset+split],
                         dmt.output_filename('Part', append=app_str))
    write_data.write_csv(config.part_plant_header.split(','),
                         part_rows[offset:offset+split],
                         dmt.output_filename('Part Plant', append=app_str))
    write_data.write_csv(config.part_rev_header.split(','),
                         part_rows[offset:offset+split],
                         dmt.output_filename('Part Revision', append=app_str))

bom_rows = [row for key in dmt_bom_data for row in dmt_bom_data[key]]
for i in range(seg_count['bom']):
    offset = i * split
    app_str = '{0}'.format(i+1)
    write_data.write_csv(Material.expected_fields,
                         bom_rows[offset:offset+split],
                         dmt.output_filename('Bill of Materials', append=app_str))

boo_rows = [row for key in dmt_boo_data for row in dmt_boo_data[key]]
for i in range(seg_count['boo']):
    offset = i * split
    app_str = '{0}'.format(i+1)
    write_data.write_csv(Operation.expected_fields,
                         boo_rows[offset:offset+split],
                         dmt.output_filename('Bill of Operations', append=app_str))

test_single_pn = 'AT11'
test_complex_pn = 'Y2233L-095-O-FRAME LF'
#debug(test_single_pn)
dmt_test(test_single_pn, test_complex_pn)
