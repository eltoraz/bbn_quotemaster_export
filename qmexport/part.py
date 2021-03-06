"""A part, as it exists in Epicor ERP
"""
from orderedset import OrderedSet
from qmexport import config
from qmexport.dmt_row import DMT_Row

class Part(DMT_Row):
    """A part, with fields from Epicor's Part, Part Revision,
    and Part Plant tables (as named in the DMT)

    Constructor arguments:
      dictionary (dict), mapping Epicor field names to values
        exported or converted from Quote Master
    """
    # these are the fields that will be passed to DMT
    #  in various iterations
    expected_fields = list(OrderedSet(config.part_header.split(',')).union(
            OrderedSet(config.part_plant_header.split(',')).union(
            OrderedSet(config.part_rev_header.split(',')))))

    def __init__(self, dictionary):
        super().__init__(dictionary)

