# dmt.py - run Epicor DMT on generated CSVs
import os
import subprocess

from qmexport import config

csv_map = {'Part': 'part.csv',
           'Part Plant': 'part_plant.csv',
           'Part Revision': 'part_rev.csv',
           'Bill of Materials': 'bom.csv',
           'Bill of Operations': 'boo.csv'}
tst_map = {'Part': 'TEST_6part.csv',
           'Part Plant': 'TEST_7part_plant.csv',
           'Part Revision': 'TEST_8part_rev.csv',
           'Bill of Materials': 'TEST_9bom.csv',
           'Bill of Operatoins': 'TEST_10boo.csv'}

def output_filename(phase, debug=False):
    """Return the path and filename for the CSV file corresponding
    to the given DMT `phase`
    """
    if debug:
        return os.path.abspath(config.output_path + tst_map[phase])
    else:
        return os.path.abspath(config.output_path + csv_map[phase])

def _dmt_cmd(phase, debug=False):
    """Return a list representing the full DMT command with all arguments
    for the given `phase` in DMT's list, to be used in subprocess.run
    """
    # DMT parameters
    dmt_exe = 'C:/Epicor/ERP10.1Client/Client/DMT.exe'
    dmt_user = '***REMOVED***'
    dmt_pass = '***REMOVED***'
    dmt_conn = 'net.tcp://server/environment'
    dmt_cnfg = 'environment'

    source = output_filename(phase, debug)

    return [dmt_exe, '-NoUI',
            '-User={0}'.format(dmt_user),
            '-Pass={0}'.format(dmt_pass),
            '-ConnectionURL="{0}"'.format(dmt_conn),
            '-ConfigValue="{0}"'.format(dmt_cnfg),
            '-Import="{0}"'.format(phase),
            '-Source="{0}"'.format(source),
            '-Add', '-Update']

def _run_dmt(phase, debug=False):
    """Execute the DMT for the given DMT `phase`
    """
    # set timeout to a sane value given the input size
    #timeout = 30

    result = subprocess.run(_dmt_cmd(phase, debug))
    return result.returncode

def run_all(debug=False):
    """Run DMT on all phases related to Quote Master data
    """
    for phase in csv_map:
        return_code = _run_dmt(phase, debug)
        if return_code:
            print('DMT error in phase', phase)
