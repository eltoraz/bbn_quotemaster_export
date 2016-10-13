# dmt.py - run Epicor DMT on generated CSVs
import os
import subprocess

from qmexport import config

csv_map = {'Part': 'part.csv',
           'Part Plant': 'part_plant.csv',
           'Part Revision': 'part_rev.csv',
           'Bill of Materials': 'bom.csv',
           'Bill of Operations': 'boo.csv'}

def output_filename(phase):
    """Return the path and filename for the CSV file corresponding
    to the given DMT `phase`
    """
    return os.path.normpath(config.output_path + csv_map[phase])

def _dmt_cmd(phase):
    """Return a string containing the full DMT command with all arguments
    for the given `phase` in DMT's list
    """
    # DMT parameters
    dmt_exe = 'C:/Epicor/ERP10.1Client/Client/DMT.exe'
    dmt_user = '***REMOVED***'
    dmt_pass = '***REMOVED***'
    dmt_conn = 'net.tcp://server/environment'
    dmt_cnfg = 'environment'

    source = output_filename(phase)

    return [dmt_exe, '-NoUI',
            '-User={0}'.format(dmt_user),
            '-Pass={0}'.format(dmt_pass),
            '-ConnectionURL="{0}"'.format(dmt_conn),
            '-ConfigValue="{0}"'.format(dmt_cnfg),
            '-Import="{0}"'.format(phase),
            '-Source="{0}"'.format(source),
            '-Add', '-Update']

def _run_dmt(phase):
    """Execute the DMT for the given DMT `phase`
    """
    # set timeout to a sane value given the input size
    #timeout = 30

    result = subprocess.run(dmt_cmd(phase))
    return result.returncode

def run_all():
    """Run DMT on all phases related to Quote Master data
    """
    for phase in csv_map:
        return_code = _run_dmt(phase)
        if return_code:
            print('DMT error in phase', phase)
