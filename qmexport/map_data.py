# convert Quote Master data to Epicor (mostly by mapping QM
#  values to their Epicor IDs)
from qmexport import config

def map_part(data):
    part_type_mapping = {'NFPPU': 'P', 'SCRNR': 'P', 'STOCK': 'P',
                         'ROCK': 'M', 'PARTS': 'M'}
    class_mapping = {'SCRNR': 'FNSH', 'ROCK': 'FSHL'} 
    class_mapping_parts = {'0': 'COMP', '-1': 'ASBL'}
    uom_mapping = {'P': 'EAP', 'M': 'EAM'}

    dmt_data = []
    for entry in data:
        dmt_entry = {}

        # derive DMT fields from QM data
        # TODO: may need to account for different description formats
        description = entry['FirstOfDesc1']
        if entry['FirstOFDesc2']:
            description = description + '_' + entry['FirstOFDesc2']
        
        classkey = entry['Inclasskey']
        class_id = class_mapping[classkey] if classkey != 'PARTS' else class_mapping_parts[entry['NRCCPrint']]

        part_type = part_type_mapping[entry['Inclasskey']]
        uom = uom_mapping[part_type]

        prefix = 'FSC' if entry['FirstOFDesc2'][:3].upper() == 'FSC' else 'NCA'
        suffix = 'ASBL' if entry['NRCCPrint'] == -1 else 'COMP'
        prod_code = prefix + '-' + suffix if part_type == 'M' else 'PURCHASE'

        # create a dict from the constants, data from QM, and data mappings
        dmt_entry['Company'] = config.company
        dmt_entry['PartNum'] = entry['Master_Plat_Part_Num']
        dmt_entry['SearchWord'] = description[:8]
        dmt_entry['PartDescription'] = description
        dmt_entry['ClassID'] = class_id
        dmt_entry['IUM'] = uom
        dmt_entry['PUM'] = uom
        dmt_entry['TypeCode'] = part_type
        dmt_entry['PricePerCode'] = config.price_per_code
        dmt_entry['ProdCode'] = prod_code
        dmt_entry['SalesUM'] = uom
        dmt_entry['UsePartRev'] = part_type == 'M'
        dmt_entry['SNFormat'] = config.sn_format if part_type == 'M' else ''
        dmt_entry['SNBaseDataType'] = config.sn_base_data_type if part_type == 'M' else ''
        dmt_entry['SNMask'] = config.sn_mask if part_type == 'M' else ''
        dmt_entry['SNMaskExample'] = config.sn_mask_example if part_type == 'M' else ''
        dmt_entry['UOMClassID'] = config.uom_class_id
        dmt_entry['NetWeightUOM'] = config.net_weight_uom if part_type == 'M' else ''

        dmt_data.append(dmt_entry)

    return dmt_data
