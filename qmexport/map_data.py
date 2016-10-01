"""convert Quote Master data to Epicor (mostly by mapping QM
values to their Epicor IDs)
"""
import re
from qmexport import config

def combined_description(entry):
    """Return the full description for the part entry, by appending
    a non-empty desc2 field to desc1, separated by an underscore
    """
    description = entry[config.desc1]
    if entry[config.desc2]:
        description = description + '_' + entry[config.desc2]

    return description

def convert_part_type(entry):
    """Return the part type based on the Platinum class key field
    """
    part_type_mapping = {'NFPPU': 'P', 'SCRNR': 'P', 'STOCK': 'P',
                         'ROCK': 'M', 'PARTS': 'M'}
    return part_type_mapping[entry[config.classkey]]

def extract_rev_num(filename):
    """Return the revision number for the part by searching the PDF
    specified by `filename`
    """
    rev_num = '00'

    return rev_num

def map_part(data):
    """Convert Quote Master part data to DMT format
    """
    class_mapping = {'SCRNR': 'FNSH', 'ROCK': 'FSHL'} 
    class_mapping_parts = {'0': 'COMP', '1': 'ASBL'}
    uom_mapping = {'P': 'EAP', 'M': 'EAM'}

    dmt_data = []
    for entry in data:
        dmt_entry = {}

        # derive DMT fields from QM data
        description = combined_description(entry)
        
        classkey = entry[config.classkey]
        class_id = class_mapping[classkey] if classkey != 'PARTS' else class_mapping_parts[entry[config.asbl_flag]]

        part_type = convert_part_type(entry)
        uom = uom_mapping[part_type]

        prefix = 'FSC' if entry[config.desc2][:3].upper() == 'FSC' else 'NCA'
        suffix = 'ASBL' if entry[config.asbl_flag] == '1' else 'COMP'
        prod_code = prefix + '-' + suffix if part_type == 'M' else 'PURCHASE'

        # create a dict from the constants, data from QM, and data mappings
        dmt_entry['Company'] = config.company
        dmt_entry['PartNum'] = entry[config.partnum]
        dmt_entry['SearchWord'] = description[:8]
        dmt_entry['PartDescription'] = description
        dmt_entry['ClassID'] = class_id
        dmt_entry['IUM'] = uom
        dmt_entry['PUM'] = uom
        dmt_entry['TypeCode'] = part_type
        dmt_entry['PricePerCode'] = config.price_per_code
        dmt_entry['ProdCode'] = prod_code
        dmt_entry['SalesUM'] = uom
        dmt_entry['UsePartRev'] = (part_type == 'M')
        dmt_entry['SNFormat'] = config.sn_format if part_type == 'M' else ''
        dmt_entry['SNBaseDataType'] = config.sn_base_data_type if part_type == 'M' else ''
        dmt_entry['SNMask'] = config.sn_mask if part_type == 'M' else ''
        dmt_entry['SNMaskExample'] = config.sn_mask_example if part_type == 'M' else ''
        dmt_entry['UOMClassID'] = config.uom_class_id
        dmt_entry['NetWeightUOM'] = config.net_weight_uom if part_type == 'M' else ''

        dmt_data.append(dmt_entry)

    return dmt_data

def map_part_prices(data):
    """Convert Quote Master part price data to DMT format, for use with DMT's
    'update' operation to add price data to already-existing parts
    """
    dmt_data = []
    for entry in data:
        dmt_entry = {}

        dmt_entry['Company'] = config.company
        dmt_entry['PartNum'] = entry[config.partnum]
        dmt_entry['PartDescription'] = combined_description(entry)
        dmt_entry['UnitPrice'] = entry['PRICE']

        dmt_data.append(dmt_entry)

    return dmt_data

def map_part_plant(data):
    """Convert Quote Master part plant data to DMT format
    """
    dmt_data = []
    for entry in data:
        dmt_entry = {}

        part_type = convert_part_type(entry)

        dmt_entry['Company'] = config.company
        dmt_entry['Plant'] = config.plant
        dmt_entry['PartNum'] = entry[config.partnum]
        dmt_entry['PrimWhse'] = config.prim_whse
        dmt_entry['SourceType'] = part_type
        dmt_entry['CostMethod'] = config.cost_method
        dmt_entry['SNMask'] = config.sn_mask if part_type == 'M' else ''
        dmt_entry['SNMaskExample'] = config.sn_mask_example if part_type == 'M' else ''
        dmt_entry['SNBaseDataType'] = config.sn_base_data_type if part_type == 'M' else ''
        dmt_entry['SNFormat'] = config.sn_format if part_type == 'M' else ''

        dmt_data.append(dmt_entry)

    return dmt_data

def map_part_rev(data):
    """Convert Quote Master part revision data to DMT format
    """
    dmt_data = []
    for entry in data:
        dmt_entry = {}

        revision_num = extract_rev_num(entry[config.print_path])
        rev_description = 'Revision ' + revision_num

        # drawing number should be in Process_Plan field, but some entries
        #  haven't been updated to new format
        proc_plan = entry[config.drawnum]
        draw_num_re = '^[a-zA-Z]{3}-\d{3}(-\w{1,2})?'

        dmt_entry['Company'] = config.company
        dmt_entry['PartNum'] = entry[config.partnum]
        dmt_entry['RevisionNum'] = revision_num
        dmt_entry['RevShortDesc'] = rev_description
        dmt_entry['RevDescription'] = rev_description
        dmt_entry['Approved'] = True
        dmt_entry['DrawNum'] = proc_plan if re.match(draw_num_re, proc_plan) else ''
        dmt_entry['Plant'] = config.plant
        dmt_entry['MtlCostPct'] = entry[config.stdcost]
        dmt_entry['ProcessMode'] = config.process_mode

        dmt_data.append(dmt_entry)

    return dmt_data
