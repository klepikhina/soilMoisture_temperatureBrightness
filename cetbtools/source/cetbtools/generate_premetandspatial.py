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
def generate_premetandspatial(cetbfilename):
    '''
    Given a CETB input file this script will generate the required
    premet and spatial data for ingest into NSIDC ECS - results go to .premet and .spatial
    files in the same directory as the input data file - per ECS requirements
    '''
    opath, datafile = os.path.split(cetbfilename)
    fd = Dataset(cetbfilename, 'r', 'NETCDF4')
    tcd = fd.getncattr('time_coverage_duration')
    duration = cetb_utilities.duration(tcd)
    if (duration):
        tcs = fd.getncattr('time_coverage_start')
        sdate, stime = cetb_utilities.datetime(tcs)
        tce = fd.getncattr('time_coverage_end')
        edate, etime = cetb_utilities.datetime(tce)
        platform = cetb_utilities.getattr(fd, 'platform', '(.+) >')
        instrument = cetb_utilities.getattr(fd, 'instrument', '(.+) >')
        epsg = cetb_utilities.getattr(fd, 'geospatial_bounds_crs', '')
        if ((epsg == "EPSG:6931") or (epsg == "EPSG:6932")):
            addattribute = "LocalTimeOfDay"
        else:
            addattribute = "AscendingDescendingFlg"
        addattributevalue = fd.variables['TB'].getncattr('temporal_division')
        lat_min = cetb_utilities.getattr(fd, 'geospatial_lat_min', '')
        lat_max = cetb_utilities.getattr(fd, 'geospatial_lat_max', '')
        lon_min = cetb_utilities.getattr(fd, 'geospatial_lon_min', '')
        lon_max = cetb_utilities.getattr(fd, 'geospatial_lon_max', '')

    fd.close()

    if (not duration):
        with open(cetbfilename+'.bad', 'w') as fb:
            fb.write("Invalid time stamps in file=%s\n" % (datafile))
            return

    with open(cetbfilename+'.premet', 'w') as fp:
        fp.write("Data_FileName=%s\n" % (datafile))
        fp.write("Begin_date=%s\n" % (sdate))
        fp.write("End_date=%s\n" % (edate))
        fp.write("Begin_time=%s\n" % (stime))
        fp.write("End_time=%s\n" % (etime))
        fp.write("Container=AssociatedPlatformInstrumentSensor\n")
        fp.write("AssociatedPlatformShortName=%s\n" % (platform))
        fp.write("AssociatedInstrumentShortName=%s\n" % (instrument))
        fp.write("AssociatedSensorShortName=%s\n" % (instrument))
        fp.write("Container=AdditionalAttributes\n")
        fp.write("AdditionalAttributeName=%s\n" % (addattribute))
        fp.write("ParameterValue=%s\n" % (addattributevalue))

    with open(cetbfilename+'.spatial', 'w') as fs:
        fs.write("%f  %f\n" % (lon_min, lat_max))
        fs.write("%f  %f\n" % (lon_max, lat_min))

if __name__ == '__main__':
    generate_premetandspatial()
