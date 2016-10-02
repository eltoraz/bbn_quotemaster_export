"""A part, as it exists in Epicor ERP
"""
from qmexport import config

class Part(object):
    """A part, with fields from Epicor's Part, Part Revision,
    and Part Plant tables (as named in the DMT)

    Constructor arguments:
      dictionary (dict), mapping Epicor field names to values
        exported or converted from Quote Master
    """
    # these are the fields that will be passed to DMT
    #  in various iterations
    expected_fields = set.union(
            set(config.part_header.split(',')),
            set(config.part_price_header.split(',')),
            set(config.part_plant_header.split(',')),
            set(config.part_rev_header.split(',')))

    def __init__(self, dictionary):
        self.update(dictionary)

    def update(self, dictionary):
        """Set the instance part's fields based on the passed-in
        dict
        """
        for k, v in dictionary.items():
            setattr(self, k, v)
