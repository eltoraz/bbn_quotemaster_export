"""convert Quote Master data to Epicor (mostly by mapping QM
values to their Epicor IDs)
"""
import re

from qmexport import config

from qmexport.part import Part

def combined_description(desc1, desc2):
    """Return the full description for the part entry, by appending
    a non-empty desc2 field to desc1, separated by an underscore
    """
    description = desc1
    if desc2:
        description = '{0}_{1}'.format(desc1, desc2)

    return description

def _map_part_base(entry):
    """Map the fields from the Part table in Epicor DMT

    Return a dict with keys as the Epicor fieldnames, mapped
    to the converted Quote Master values
    """
    dmt_entry = {}

    # derive DMT fields from QM data
    description = combined_description(entry[config.desc1], entry[config.desc2])

    classkey = entry[config.classkey]
    if classkey != 'PARTS':
        class_id = config.class_mapping.get(classkey, '!{0}!'.format(classkey))
    else:
        class_id = config.class_mapping_parts[entry[config.asbl_flag]]

    # default part type is 'P' (raw material), since there are so many
    part_type = config.part_type_mapping.get(entry[config.classkey], 'P')
    uom = config.uom_mapping[part_type]

    prefix = 'FSC' if entry[config.desc2][:3].upper() == 'FSC' else 'NCA'
    suffix = 'ASBL' if entry[config.asbl_flag] == '1' else 'COMP'
    prod_code = prefix + '-' + suffix if part_type == 'M' else 'PURCHASE'

    # create a dict from the constants, data from QM, and data mappings
    dmt_entry['Company'] = config.company
    dmt_entry['PartNum'] = entry[config.partnum]
    dmt_entry['SearchWord'] = description[:8].strip()
    dmt_entry['PartDescription'] = description
    dmt_entry['ClassID'] = class_id
    dmt_entry['IUM'] = uom
    dmt_entry['PUM'] = uom
    dmt_entry['TypeCode'] = part_type
    dmt_entry['NonStock'] = True
    dmt_entry['PricePerCode'] = config.price_per_code
    dmt_entry['ProdCode'] = prod_code
    dmt_entry['CostMethod'] = config.cost_method[part_type]
    dmt_entry['TrackLots'] = True if part_type == 'P' else False
    dmt_entry['SalesUM'] = uom
    dmt_entry['UsePartRev'] = (part_type == 'M')
    dmt_entry['SNFormat'] = config.sn_format if part_type == 'M' else ''
    dmt_entry['SNBaseDataType'] = config.sn_base_data_type if part_type == 'M' else ''
    dmt_entry['SNMask'] = config.sn_mask if part_type == 'M' else ''
    dmt_entry['SNMaskExample'] = config.sn_mask_example if part_type == 'M' else ''
    dmt_entry['UOMClassID'] = config.uom_class_id
    dmt_entry['NetWeightUOM'] = config.net_weight_uom if part_type == 'M' else ''

    return dmt_entry

def _map_part_plnt(entry):
    """Map the fields from the Part Plant table in Epicor DMT

    Return a dict with keys as the Epicor fieldnames, mapped
    to the converted Quote Master values
    """
    dmt_entry = {}
    part_type = config.part_type_mapping.get(entry[config.classkey], 'P')

    dmt_entry['Plant'] = config.plant
    dmt_entry['PrimWhse'] = config.prim_whse
    dmt_entry['SourceType'] = part_type

    return dmt_entry

def _map_part_revn(entry):
    """Map the fields from the Part Revision table in Epicor DMT

    Aside from the entry, takes a dictionary of parts->rev num

    Return a dict with keys as the Epicor fieldnames, mapped
    to the converted Quote Master values
    """
    dmt_entry = {}

    # drawing number should be in Process_Plan field, but some entries
    #  haven't been updated to new format
    proc_plan = entry[config.drawnum]
    draw_num_re = '([a-zA-Z]{3}-\d{3})'
    draw_num_match = re.match(draw_num_re, proc_plan)

    revision_num = ''

    dmt_entry['RevisionNum'] = revision_num
    dmt_entry['RevShortDesc'] = 'Revision ' + revision_num
    dmt_entry['Approved'] = True
    dmt_entry['DrawNum'] = draw_num_match.group(1) if draw_num_match else ''
    dmt_entry['ProcessMode'] = config.process_mode

    return dmt_entry

def map_part(data):
    """Convert Quote Master part data to DMT format
    Return a dictionary mapping part numbers to Part objects
    """
    dmt_data = {}
    for entry in data:
        working_part = Part(_map_part_base(entry))
        working_part.update(_map_part_plnt(entry))
        working_part.update(_map_part_revn(entry))

        dmt_data[working_part.PartNum] = working_part

    return dmt_data
