output_path = 'output/'
csv_path = 'ref/'
csv_files = {'part': '20161007_1140_qm_part_query_all.csv',
             'bill of materials': '20161007_1224_qm_bom_query.csv',
             'bill of operations': '20161007_1225_qm_boo_query.csv',
             'part revision': 'part_rev_test.csv'}

def qualified_filename(query):
    """Return the path and filename for the specified reference file
    """
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

operation_mapping = {}

# query field names                   table of origin
partnum = 'Itemkey'                 # Item Master
desc1 = 'Itemdescription1'          # Item Master
desc2 = 'Itemdescription2'          # Item Master
classkey = 'Itemclasskey'           # Item Location
asbl_flag = 'NRCCPrint'             # QuoteMaster Main
stdcost = 'Standardcost'            # Item Location
drawnum = 'Process_Plan'            # QuoteMaster Main
image_path = 'Image_Path'           # 3901_tbl_Blueprint_Path
mtl_partnum = 'Plat_Item_Num'       # QM BOM
qty_per = 'QTY'                     # QM BOM
opr_seq = 'Sequence_Number'         # QM BOO
op_code = 'MACHINE_Center'          # QM BOO
op_desc = 'Process - DESC'          # QM BOO

# CSV headers
part_header = (
        'Company,PartNum,SearchWord,PartDescription,ClassID,IUM,PUM,'
        'TypeCode,PricePerCode,ProdCode,SalesUM,UsePartRev,ImageFileName,'
        'SNFormat,SNBaseDataType,SNMask,SNMaskExample,UOMClassID,NetWeightUOM')
part_plant_header = (
        'Company,Plant,PartNum,PrimWhse,SourceType,CostMethod,SNMask,'
        'SNMaskExample,SNBaseDataType,SNFormat')
part_rev_header = (
        'Company,PartNum,RevisionNum,RevShortDesc,'
        'Approved,DrawNum,Plant,ProcessMode')
bom_header = (
        'Company,PartNum,RevisionNum,MtlSeq,MtlPartNum,QtyPer,'
        'Plant,ECOGroupID')
boo_header = (
        'Company,PartNum,RevisionNum,OprSeq,OpCode,OpDesc,Plant,ECOGroupID')
