"""Convert Quote Master material data to an Epicor-friendly format
by mapping QM values to their Epicor IDs
"""
from qmexport import config

from qmexport.material import Material

def _map_material(entry, mtl_seq, rev_dict):
    """Map the fields from the Bill of Materials table in Epicor DMT

    Return a dict with keys as the Epicor fieldnames, mapped to the
    converted values from Quote Master
    """
    dmt_entry = {}

    dmt_entry['Company'] = config.company
    dmt_entry['PartNum'] = entry[config.partnum]
    dmt_entry['RevisionNum'] = rev_dict.get(entry[config.partnum], '')
    dmt_entry['MtlSeq'] = mtl_seq
    dmt_entry['MtlPartNum'] = entry[config.mtl_partnum]
    dmt_entry['QtyPer'] = round(1.0 / float(entry[config.qty_per]))
    dmt_entry['Plant'] = config.plant
    dmt_entry['ECOGroupID'] = config.eco_group_id

    return dmt_entry

def map_bom(data, rev_dict):
    """Convert Quote Master supply data to DMT format for bill of materials

    Return a dictionary mapping part numbers to a list of Material objects
    corresponding to that part
    """
    dmt_data = {}
    for entry in data:
        # TODO: need to make sure dropping the entry is desired behavior
        if float(entry[config.qty_per]) == 0.0:
            continue

        mtl_seq = (len(dmt_data.get(entry[config.partnum], [])) + 1) * 10
        working_material = Material(_map_material(entry, mtl_seq, rev_dict))

        if entry[config.partnum] in dmt_data:
            dmt_data[entry[config.partnum]].append(working_material)
        else:
            dmt_data[entry[config.partnum]] = [working_material]

    return dmt_data
