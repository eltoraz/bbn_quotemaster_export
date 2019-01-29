import argparse

import qmexport
import qmexport.dmt

test_single_pn = 'AT11'
test_complex_pn = 'Y2233L-095-O-FRAME LF'

def _test(delete):
    """Run DMT on test data, passing the `delete` parameter through to
    determine whether to run Add/Update or Delete operations
    """
    qmexport.dmt_test(test_single_pn, test_complex_pn, delete)

def _full(delete):
    """Run DMT on live data, passing the `delete` parameter through to
    determine whether to run Add/Update or Delete operations
    """
    qmexport.dmt.run_all(qmexport.seg_count, delete=delete)

parser = argparse.ArgumentParser(
        description='Export data from Quote Master into Epicor.')

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
    _test(args.delete)
else:
    _full(args.delete)
