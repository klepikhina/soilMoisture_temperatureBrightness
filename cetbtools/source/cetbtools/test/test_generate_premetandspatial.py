'''
Nose tests for premet-gen package

To run tests : fab [-v] test.all

'''
from __future__ import print_function

from click.testing import CliRunner
from nose.tools import assert_equals
import os
import sys

from cetbtools.generate_premetandspatial import generate_premetandspatial
from cetbtools.generate_bad_premetandspatial import generate_bad_premetandspatial


def test_with_no_filename():
    runner = CliRunner()
    result = runner.invoke(generate_premetandspatial)
    assert_equals(result.exit_code, 2)
    assert "Missing argument" in result.output


def test_with_bad_filename():
    runner = CliRunner()
    result = runner.invoke(generate_premetandspatial, ['bogus'])
    assert_equals(result.exit_code, 2)
    assert "does not exist" in result.output


def test_with_N_filename():
    runner = CliRunner()
    prefix = 'NSIDC-0630-EASE2'
    N_filename = os.path.join('/projects/PMESDR/vagrant/test_cetbtools_data/',
                              '%s_N6.25km-AQUA_AMSRE-2008278-18H-M-SIR-RSS-v1.0.nc'
                              % (prefix))
    result = runner.invoke(generate_premetandspatial, [N_filename])
    print(result.output, file=sys.stderr)
    with open(N_filename+'.premet', 'r') as fp:
        lines = fp.readlines()
    assert "Data_FileName=%s" % (prefix) in lines[0]
    assert "Begin_date=2008-10-04" in lines[1]
    assert "End_date=2008-10-05" in lines[2]
    assert "Begin_time=00:05:00.00" in lines[3]
    assert "End_time=00:49:00.00" in lines[4]
    assert "Container=AssociatedP" in lines[5]
    assert "AssociatedPlatformShortName=AQUA" in lines[6]
    assert "AssociatedInstrumentShortName=A" in lines[7]
    assert "AssociatedSensorShortName=A" in lines[8]
    assert "AdditionalAttributeName" in lines[10]
    assert "ParameterValue=" in lines[11]


def test_with_bad_duration_filename():
    runner = CliRunner()
    prefix = 'NSIDC-0630-EASE2'
    N_filename = os.path.join('/projects/PMESDR/vagrant/test_cetbtools_data/',
                              '%s_N25km-AQUA_AMSRE-2002211-23V-E-GRD-RSS-v1.0.nc'
                              % (prefix))
    result = runner.invoke(generate_premetandspatial, [N_filename])
    print(result.output, file=sys.stderr)
    with open(N_filename+'.bad', 'r') as fp:
        lines = fp.readlines()
    assert "Invalid time stamps in file=%s" % (prefix) in lines[0]


def test_generate_bad_premetandspatial():
    runner = CliRunner()
    prefix = 'NSIDC-0630-EASE2'
    N_filename = os.path.join('/projects/PMESDR/vagrant/test_cetbtools_data/',
                              '%s_N25km-AQUA_AMSRE-2002211-23V-E-GRD-RSS-v1.0.nc'
                              % (prefix))
    result = runner.invoke(generate_bad_premetandspatial, [N_filename])
    print(result.output, file=sys.stderr)
    with open(N_filename+'.bad', 'r') as fp:
        lines = fp.readlines()
    assert "Invalid time stamps in file=%s" % (prefix) in lines[0]
