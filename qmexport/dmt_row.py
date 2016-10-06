"""A data structure to represent a row (with column names)
in Epicor ERP, for import using DMT
"""
from qmexport import config

class DMT_Row(object):
    """A generic row to pass to DMT - use the subclasses instead

    Constructor arguments:
      dictionary (dict), mapping Epicor field names to values
        exported or converted from Quote Master
    """
    def __init__(self, dictionary):
        self.update(dictionary)

    def __repr__(self):
        return self.__dict__.__repr__()

    def update(self, dictionary):
        """Set the instance part's fields based on the passed-in
        dict
        """
        for k, v in dictionary.items():
            setattr(self, k, v)
