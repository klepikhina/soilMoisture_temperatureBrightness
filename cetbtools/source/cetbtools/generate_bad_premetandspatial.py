#!/usr/bin/env python
from __future__ import print_function
import cetb_utilities  # noqa
import click  # noqa
from netCDF4 import Dataset  # noqa
import os   # noqa
import re   # noqa
import sys   # noqa


@click.command()
@click.argument('cetbfilename', type=click.Path(exists=True))
def generate_bad_premetandspatial(cetbfilename):
    '''
    Given a CETB input file this script will check for bad date ranges and
    write out a file.bad if such is found - skips over all other files
    this makes it easier to eliminate the empty files if needed
    '''
    opath, datafile = os.path.split(cetbfilename)
    fd = Dataset(cetbfilename, 'r', 'NETCDF4')
    tcd = fd.getncattr('time_coverage_duration')
    duration = cetb_utilities.duration(tcd)
    fd.close()

    if (not duration):
        with open(cetbfilename+'.bad', 'w') as fb:
            fb.write("Invalid time stamps in file=%s\n" % (datafile))
            return

if __name__ == '__main__':
    generate_bad_premetandspatial()
