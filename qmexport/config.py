output_path = 'output/'
csv_path = 'ref/'
csv_files = {'part': '20161003_1343_qm_part_query_all.csv',
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

# constants dependent on part type 
sn_format = 'NF#######'
sn_base_data_type = 'MASK'
sn_mask = 'NF'
sn_mask_example = 'NF9999999'
net_weight_uom = 'LB'

# Quote Master -> Epicor mappings
class_mapping = {'SCRNR': 'FNSH', 'ROCK': 'FSHL'}
class_mapping_parts = {'0': 'COMP', '1': 'ASBL'}
uom_mapping = {'P': 'EAP', 'M': 'EAM'}
part_type_mapping = {'NFPPU': 'P', 'SCRNR': 'P', 'STOCK': 'P',
                     'ROCK': 'M', 'PARTS': 'M'}

# query field names                   table of origin
partnum = 'Master_Plat_Part_Num'    # QuoteMaster Main
desc1 = 'FirstOfDesc1'              # 102_tbl_Iloc_Local
desc2 = 'FirstOFDesc2'              # 102_tbl_Iloc_Local ('OF' not 'Of')
classkey = 'Inclasskey'             # 102_tbl_Iloc_Local
asbl_flag = 'NRCCPrint'             # QuoteMaster Main
stdcost = 'FirstOfStdcost'          # 102_tbl_Iloc_Local
drawnum = 'Process_Plan'            # QuoteMaster Main
print_path = 'Image_Path'           # 3901_tbl_Blueprint_Path
unit_price = 'PRICE'                # QM BOM

# CSV headers
part_header = (
        'Company,PartNum,SearchWord,PartDescription,ClassID,IUM,PUM,'
        'TypeCode,UnitPrice,PricePerCode,ProdCode,SalesUM,UsePartRev,'
        'SNFormat,SNBaseDataType,SNMask,SNMaskExample,UOMClassID,NetWeightUOM')
part_plant_header = (
        'Company,Plant,PartNum,PrimWhse,SourceType,CostMethod,SNMask,'
        'SNMaskExample,SNBaseDataType,SNFormat')
part_rev_header = (
        'Company,PartNum,RevisionNum,RevShortDesc,'
        'Approved,DrawNum,Plant,MtlCostPct,ProcessMode')
bom_header = (
        'Company,PartNum,RevisionNum,MtlSeq,MtlPartNum,QtyPer,'
        'Plant,ECOGroupID')

# dummy print file
dummy_print = '\\\\poplar\\bbn_common\\PDFPrints\\Customer\\No_Print.pdf'
