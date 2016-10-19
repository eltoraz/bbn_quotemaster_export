# dmt.py - run Epicor DMT on generated CSVs
import os
import subprocess

from collections import OrderedDict

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

def _dmt_cmd(phase, seg, debug=False):
    """Return a list representing the full DMT command with all arguments
    for the given `phase` in DMT's list, to be used in subprocess.run

    Since the data may be in segments, `seg` represents the current chunk
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
            '-Source="{0}"'.format(source),
            '-Add', '-Update']

def _run_dmt(phase, seg_count, debug=False):
    """Execute the DMT for the given DMT `phase`
    """
    # set timeout to a sane value given the input size
    #timeout = 30

    return_code = 0
    for i in range(seg_count):
        log.log('Running DMT on phase ' + phase + ', segment ' + str(i+1) +
                ' of ' + str(seg_count) + ' (debug={0})'.format(debug))
        result = subprocess.run(_dmt_cmd(phase, i+1, debug))
        if result.returncode:
            return_code = 1
            log.log('DMT error in phase ' + phase + ', segment ' + str(i+1))

    return return_code

def run_all(seg_count, debug=False):
    """Run DMT on all phases related to Quote Master data
    """
    # part/plant/rev all should have the same # of segments since they're
    # built from the same data
    seg_count_map = {'Part': 'part',
                     'Part Plant': 'part',
                     'Part Revision': 'part',
                     'Bill of Materials': 'bom',
                     'Bill of Operations': 'boo'}

    for phase in csv_map:
        return_code = _run_dmt(phase, seg_count[seg_count_map[phase]], debug)
