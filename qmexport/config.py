output_path = 'output/'
csv_path = 'ref/'
csv_files = {'part': '20160930_1036_qm_part_query.csv',
             'part price': '20160930_1048_qm_part_prices_query.csv',
             'part revision': '20160930_1503_qm_part_rev_query.csv',
             'bill of materials': '',
             'bill of operations': ''}

def qualified_filename(query):
    return csv_path + csv_files[query]

# constants
company = 'BBN'
price_per_code = 'E'
use_part_rev = True
uom_class_id = 'BBN'

plant = 'MfgSys'
process_mode = 'S'

prim_whse = 453
cost_method = 'F'

eco_group_id = 'DMT'

# constants dependent on part type (they'll have either this value or '')
sn_format = 'NF#######'
sn_base_data_type = 'MASK'
sn_mask = 'NF'
sn_mask_example = 'NF9999999'
net_weight_uom = 'LB'

# CSV headers
part_header = (
        'Company,PartNum,SearchWord,PartDescription,ClassID,IUM,PUM,'
        'TypeCode,PricePerCode,ProdCode,SalesUM,UsePartRev,SNFormat,'
        'SNBaseDataType,SNMask,SNMaskExample,UOMClassID,NetWeightUOM')
part_price_header = 'Company,PartNum,PartDescription,UnitPrice'
part_plant_header = (
        'Company,Plant,PartNum,PrimWhse,SourceType,CostMethod,SNMask,'
        'SNMaskExample,SNBaseDataType,SNFormat')
part_rev_header = (
        'Company,PartNum,RevisionNum,RevShortDesc,RevDescription,'
        'Approved,DrawNum,Plant,MtlCostPct,ProcessMode')
bom_header = (
        'Company,PartNum,RevisionNum,MtlSeq,MtlPartNum,QtyPer,'
        'Plant,ECOGroupID')

# dummy print file
dummy_print = '\\\\poplar\\bbn_common\\PDFPrints\\Customer\\No_Print.pdf'
