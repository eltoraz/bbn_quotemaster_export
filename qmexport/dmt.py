# dmt.py - run Epicor DMT on generated CSVs
import os
import subprocess

from collections import OrderedDict
from copy import copy

from qmexport import config, log

# need to use an ordered dict, since the order of the DMT phases
#  is important
keys = ['Part', 'Part Plant', 'Part Revision',
        'Bill of Materials', 'Bill of Operations']
csv_map = OrderedDict.fromkeys(keys)
tst_map = OrderedDict.fromkeys(keys)

# old dict literals
csv_fil = {'Part': 'part',
           'Part Plant': 'part_plant',
           'Part Revision': 'part_rev',
           'Bill of Materials': 'bom',
           'Bill of Operations': 'boo'}
tst_fil = {'Part': 'TEST_6part',
           'Part Plant': 'TEST_7part_plant',
           'Part Revision': 'TEST_8part_rev',
           'Bill of Materials': 'TEST_9bom',
           'Bill of Operations': 'TEST_10boo'}

for key in keys:
    csv_map[key] = csv_fil[key]
    tst_map[key] = tst_fil[key]

def output_filename(phase, debug=False, append=''):
    """Return the path and filename for the CSV file corresponding
    to the given DMT `phase`
    """
    suffix = ''
    if append:
        suffix = '_{0}'.format(append)

    if debug:
        filename = os.path.abspath(config.output_path + tst_map[phase])
    else:
        filename = os.path.abspath(config.output_path + csv_map[phase])

    return filename + suffix + '.csv'

def _dmt_cmd(phase, seg, ops, debug=False):
    """Return a list representing the full DMT command with all arguments
    for the given `phase` in DMT's list, to be used in subprocess.run

    Since the data may be in segments, `seg` represents the current chunk

    `ops` should be specified as a list of arguments to choose DMT's
    behavior (e.g., specify ['-Delete'] to remove records from the DB)
    """
    # DMT parameters
    dmt_exe = 'C:/Epicor/ERP10.1Client/Client/DMT.exe'
    dmt_user = '***REMOVED***'
    dmt_pass = '***REMOVED***'
    dmt_conn = 'net.tcp://server/environment'
    dmt_cnfg = 'environment'

    source = output_filename(phase, debug, seg)

    return [dmt_exe, '-NoUI',
            '-User={0}'.format(dmt_user),
            '-Pass={0}'.format(dmt_pass),
            '-ConnectionURL="{0}"'.format(dmt_conn),
            '-ConfigValue="{0}"'.format(dmt_cnfg),
            '-Import="{0}"'.format(phase),
            '-Source="{0}"'.format(source)] + ops

def _run_dmt(phase, seg_count, delete=False, debug=False):
    """Execute the DMT for the given DMT `phase`

    If `delete` is set to True, call the DMT to remove the records in
    the target CSV from Epicor's DB
    """
    peak_rpm = 200          # estimated DMT peak records per minute
    leeway = 1.4

    # timeout based on the max # of records per file and DMT's
    #  throughput rate, with a little extra leeway
    timeout = config.split / (peak_rpm / 60) * leeway

    # operation arguments to pass to DMT
    ops = ['-Add', '-Update']
    if delete:
        ops = ['-Delete']

    # run DMT on each CSV containing a subset of data for the given phase
    return_code = 0
    for i in range(seg_count):
        try:
            result = subprocess.run(_dmt_cmd(phase, i+1, ops, debug), timeout=timeout)
        except TimeoutExpired as err:
            return_code = -1
            log.log('DMT timed out ({0} sec) in phase {1}, segment {2}'.format(
                    err.timeout, phase, i+1))
        else:
            return_code = result.returncode

        if return_code == 0:
            log.log(('DMT successfully completed {0}, segment {1} of '
                     '{2} (debug={3})').format(phase, i+1, seg_count, debug))
        elif return_code == 1:
            log.log('DMT error in phase {0}, segment {1}'.format(phase, i+1))

    return return_code

def run_all(seg_count, debug=False, delete=False):
    """Run DMT on all phases related to Quote Master data
    """
    # part/plant/rev all should have the same # of segments since they're
    # built from the same data
    seg_count_map = {'Part': 'part',
                     'Part Plant': 'part',
                     'Part Revision': 'part',
                     'Bill of Materials': 'bom',
                     'Bill of Operations': 'boo'}

    # need to reverse order of operations if deleting records
    key_order = copy(keys)
    if delete:
        key_order.reverse()

    for phase in key_order:
        return_code = _run_dmt(phase, seg_count[seg_count_map[phase]],
                               delete=delete, debug=debug)
