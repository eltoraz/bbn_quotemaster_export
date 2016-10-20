import argparse

import qmexport

test_single_pn = 'AT11'
test_complex_pn = 'Y2233L-095-O-FRAME LF'

def _test_add():
    """Run DMT Add & Update on test data
    """
    qmexport.dmt_test(test_single_pn, test_complex_pn)

def _test_del():
    """Run DMT Delete on test data (usually to clear it from the DB
    to test changes to Add)
    """
    qmexport.dmt_test(test_single_pn, test_complex_pn, True)

def _full_add():
    """Run DMT Add & Update on live data
    """
    pass

def _full_del():
    """Run DMT Delete on live data
    """
    pass

parser = argparse.ArgumentParser(description=('Export data from Quote '
                                              'Master into Epicor.'))
parser.add_argument('--debug', action='store_true',
                    help='print debug info on data collected')
parser.add_argument('--test', action='store_true',
                    help='run operations on small test datasets')
parser.add_argument('--delete', action='store_true',
                    help='remove data from the DB instead')

args = parser.parse_args()

if args.debug:
    qmexport.debug(test_single_pn)

# run the operation determined by the arguments given
if args.test:
    if args.delete:
        _test_del()
    else:
        _test_add()
else:
    if args.delete:
        _full_del()
    else:
        _full_add()
