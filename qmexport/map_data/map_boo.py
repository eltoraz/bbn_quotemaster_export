"""Convert Quote Master operation data to an Epicor-friendly format
by mapping QM values to their Epicor IDs
"""
from qmexport import config

from qmexport.operation import Operation

def _map_operation(entry, rev_dict):
    """Map the fields from the Bill of Operations in Epicor DMT

    Return a dict with keys as the Epicor fieldnames, mapped to the
    converted values from Quote Master
    """
    dmt_entry = {}

    # default op when not in the mapping is 'Assembly Step 1'
    fallback_op = '110-1'

    # TODO: OpDesc caps at 30char
    dmt_entry['Company'] = config.company
    dmt_entry['PartNum'] = entry[config.partnum]
    dmt_entry['RevisionNum'] = rev_dict.get(entry[config.partnum], '')
    dmt_entry['OprSeq'] = entry[config.opr_seq]
    dmt_entry['OpCode'] = config.operation_mapping.get(entry[config.op_code], fallback_op)
    dmt_entry['OpDesc'] = entry[config.op_desc][:29]
    dmt_entry['Plant'] = config.plant
    dmt_entry['ECOGroupID'] = config.eco_group_id

    return dmt_entry

def map_boo(data, rev_dict):
    """Convert Quote Master process plan data to DMT format for
    bill of operations

    Return a dictionary mapping part numbers to a list of Operation
    objects corresponding to that part
    """
    dmt_data = {}
    for entry in data:
        working_operation = Operation(_map_operation(entry, rev_dict))

        if entry[config.partnum] in dmt_data:
            dmt_data[entry[config.partnum]].append(working_operation)
        else:
            dmt_data[entry[config.partnum]] = [working_operation]

    return dmt_data
