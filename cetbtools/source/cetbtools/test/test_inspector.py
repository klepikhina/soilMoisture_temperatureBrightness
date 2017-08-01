'''
Nose tests for inspector package

To run tests : fab [-v] test.all

'''
from __future__ import print_function

import glob
import os
import sys

from nose.tools import assert_raises, ok_

from cetbtools.inspector import make_cetb_geotiff
from cetbtools.inspector import make_cetb_png

verbose = False
test_data_dir = "/projects/PMESDR/vagrant/test_cetbtools_data"


def test_png_loop_grids():
    list = glob.glob("%s/NSIDC-0630-EASE2_T3*89V-A*.nc" % test_data_dir)
    for file in list:
        print("Next: %s" % (file), file=sys.stderr)
        make_cetb_png(file, verbose=True)


def test_make_cetb_png_bogus_file():
    assert_raises(IOError, make_cetb_png, "bogus.nc")


def test_make_cetb_png_TB():
    filename = os.path.join(test_data_dir,
                            'EASE2_N25km.F13_SSMI.2003001.37H.E.GRD.CSU.v0.1.nc')
    ok_(make_cetb_png(filename, verbose=verbose))


def test_make_cetb_png_TB_std_dev():
    filename = os.path.join(test_data_dir,
                            'EASE2_N25km.F13_SSMI.2003001.37H.E.GRD.CSU.v0.1.nc')
    ok_(make_cetb_png(filename, var_name="TB_std_dev", verbose=verbose))


def test_make_cetb_png_TB_time():
    filename = os.path.join(test_data_dir,
                            'EASE2_N25km.F13_SSMI.2003001.37H.E.GRD.CSU.v0.1.nc')
    ok_(make_cetb_png(filename, var_name="TB_time", verbose=verbose))


def test_make_cetb_png_TB_num_samples():
    filename = os.path.join(test_data_dir,
                            'EASE2_N25km.F13_SSMI.2003001.37H.E.GRD.CSU.v0.1.nc')
    ok_(make_cetb_png(filename, var_name="TB_num_samples", verbose=verbose))


def test_make_cetb_png_Incidence_angle():
    filename = os.path.join(test_data_dir,
                            'EASE2_N25km.F13_SSMI.2003001.37H.E.GRD.CSU.v0.1.nc')
    ok_(make_cetb_png(filename, var_name="Incidence_angle", verbose=verbose))


def test_make_cetb_geotiff_bogus_file():
    assert_raises(IOError, make_cetb_geotiff, "bogus.nc")


def test_make_cetb_geotiff_TB():
    filename = os.path.join(test_data_dir,
                            'EASE2_N25km.F13_SSMI.1997061.19H.E.GRD.CSU.v0.1.nc')
    ok_(make_cetb_geotiff(filename, verbose=verbose))


def test_make_cetb_geotiff_TB_std_dev():
    filename = os.path.join(test_data_dir,
                            'EASE2_N25km.F13_SSMI.1997061.19H.E.GRD.CSU.v0.1.nc')
    ok_(make_cetb_geotiff(filename, var_name="TB_std_dev", verbose=verbose))


def test_make_cetb_geotiff_TB_time():
    filename = os.path.join(test_data_dir,
                            'EASE2_N25km.F13_SSMI.1997061.19H.E.GRD.CSU.v0.1.nc')
    ok_(make_cetb_geotiff(filename, var_name="TB_time", verbose=verbose))


def test_make_cetb_geotiff_TB_num_samples():
    filename = os.path.join(test_data_dir,
                            'EASE2_N25km.F13_SSMI.1997061.19H.E.GRD.CSU.v0.1.nc')
    ok_(make_cetb_geotiff(filename, var_name="TB_num_samples", verbose=verbose))


def test_make_cetb_geotiff_Incidence_angle():
    filename = os.path.join(test_data_dir,
                            'EASE2_N25km.F13_SSMI.1997061.19H.E.GRD.CSU.v0.1.nc')
    ok_(make_cetb_geotiff(filename, var_name="Incidence_angle", verbose=verbose))
