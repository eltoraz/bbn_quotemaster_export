"""An operation, as it exists in the Bill of Operations table in Epicor ERP
"""
from orderedset import OrderedSet
from qmexport import config
from qmexport.dmt_row import DMT_Row

class Operation(DMT_Row):
    """An operation entry in an Epicor ERP bill of operations

    Constructor arguments:
      dictionary (dict), mapping Epicor field names to values
        exported or converted from Quote Master
    """
    # these are the fields that will be passed to DMT
    #  in various iterations
    expected_fields = list(OrderedSet(config.boo_header.split(',')))

    def __init__(self, dictionary):
        super().__init__(dictionary)
