'''
Nose tests for ease2conv package

To run tests : fab [-v] test.all

'''
from __future__ import print_function

from cetbtools.ease2conv import Ease2Transform
from nose.tools import assert_is, assert_almost_equals, assert_raises

verbose = False
precision6 = 6
precision5 = 5
precision4 = 4


def test_Ease2Transform_init_bogus():
    assert_raises(ValueError, Ease2Transform, "bogus")


def test_Ease2Transform_init():
    Ngrid = Ease2Transform("EASE2_N25km")
    assert_is(Ngrid.gridname, "EASE2_N25km")
    N31grid = Ease2Transform("EASE2_N3.125km")
    assert_is(N31grid.gridname, "EASE2_N3.125km")
    Sgrid = Ease2Transform("EASE2_S25km")
    assert_is(Sgrid.gridname, "EASE2_S25km")
    Tgrid = Ease2Transform("EASE2_T25km")
    assert_is(Tgrid.gridname, "EASE2_T25km")


def test_origin_Ease2Transform_grid_to_map():
    Ngrid = Ease2Transform("EASE2_N25km")
    x, y = Ngrid.grid_to_map(359.5, 359.5)
    assert_almost_equals(x, 0., places=precision6)
    assert_almost_equals(y, 0., places=precision6)
    Sgrid = Ease2Transform("EASE2_S25km")
    x, y = Sgrid.grid_to_map(359.5, 359.5)
    assert_almost_equals(x, 0., places=precision6)
    assert_almost_equals(y, 0., places=precision6)
    Tgrid = Ease2Transform("EASE2_T25km")
    x, y = Tgrid.grid_to_map(269.5, 693.5)
    assert_almost_equals(x, 0., places=precision6)
    assert_almost_equals(y, 0., places=precision6)


def test_UL_Ease2Transform_grid_to_map():
    Ngrid = Ease2Transform("EASE2_N25km")
    x, y = Ngrid.grid_to_map(-0.5, -0.5)
    assert_almost_equals(x, -9000000., places=precision6)
    assert_almost_equals(y, 9000000., places=precision6)
    Sgrid = Ease2Transform("EASE2_S25km")
    x, y = Sgrid.grid_to_map(-0.5, -0.5)
    assert_almost_equals(x, -9000000., places=precision6)
    assert_almost_equals(y, 9000000., places=precision6)
    Tgrid = Ease2Transform("EASE2_T25km")
    x, y = Tgrid.grid_to_map(-0.5, -0.5)
    assert_almost_equals(x, -17367530.44, places=precision6)
    assert_almost_equals(y, 6756820.2, places=precision6)


# Test origins and UL corners of each projection
def test_origin_Ease2Transform_grid_to_geographic():
    Ngrid = Ease2Transform("EASE2_N25km")
    lat, lon = Ngrid.grid_to_geographic(359.5, 359.5)
    assert_almost_equals(lat, 90., places=precision6)
    assert_almost_equals(lon, 0., places=precision6)
    lat, lon = Ngrid.grid_to_geographic(-0.5, -0.5)
    assert_almost_equals(lat, -84.634050, places=precision6)
    assert_almost_equals(lon, -135., places=precision6)

    Sgrid = Ease2Transform("EASE2_S25km")
    lat, lon = Sgrid.grid_to_geographic(359.5, 359.5)
    assert_almost_equals(lat, -90., places=precision6)
    assert_almost_equals(lon, 0., places=precision6)
    lat, lon = Sgrid.grid_to_geographic(-0.5, -0.5)
    assert_almost_equals(lat, 84.634050, places=precision6)
    assert_almost_equals(lon, -45., places=precision6)

    Tgrid = Ease2Transform("EASE2_T25km")
    lat, lon = Tgrid.grid_to_geographic(269.5, 693.5)
    assert_almost_equals(lat, 0., places=precision6)
    assert_almost_equals(lon, 0., places=precision6)
    lat, lon = Tgrid.grid_to_geographic(-0.5, -0.5)
    assert_almost_equals(lat, 67.057541, places=precision6)
    assert_almost_equals(lon, -180., places=precision6)


def test_high_res_Ease2Transform_grid_to_geographic():
    Ngrid = Ease2Transform("EASE2_N3.125km")
    lat, lon = Ngrid.grid_to_geographic(-0.5, -0.5)
    assert_almost_equals(lat, -84.634050, places=precision6)
    assert_almost_equals(lon, -135., places=precision6)
    Sgrid = Ease2Transform("EASE2_S6.25km")
    lat, lon = Sgrid.grid_to_geographic(-0.5, -0.5)
    assert_almost_equals(lat, 84.634050, places=precision6)
    assert_almost_equals(lon, -45., places=precision6)
    Tgrid = Ease2Transform("EASE2_T12.5km")
    lat, lon = Tgrid.grid_to_geographic(-0.5, -0.5)
    assert_almost_equals(lat, 67.057541, places=precision6)
    assert_almost_equals(lon, -180., places=precision6)


def test_origin_Ease2Transform_map_to_grid():
    Ngrid = Ease2Transform("EASE2_N25km")
    row, col = Ngrid.map_to_grid(0., 0.)
    assert_almost_equals(row, 359.5, places=precision6)
    assert_almost_equals(col, 359.5, places=precision6)
    Sgrid = Ease2Transform("EASE2_S25km")
    row, col = Sgrid.map_to_grid(0., 0.)
    assert_almost_equals(row, 359.5, places=precision6)
    assert_almost_equals(col, 359.5, places=precision6)
    Tgrid = Ease2Transform("EASE2_T25km")
    row, col = Tgrid.map_to_grid(-17367530.44, 6756820.2)
    assert_almost_equals(row, -0.5, places=precision6)
    assert_almost_equals(col, -0.5, places=precision6)


def test_UL_Ease2Transform_map_to_grid():
    Ngrid = Ease2Transform("EASE2_N25km")
    row, col = Ngrid.map_to_grid(-9000000., 9000000.)
    assert_almost_equals(row, -0.5, places=precision6)
    assert_almost_equals(col, -0.5, places=precision6)
    Sgrid = Ease2Transform("EASE2_S25km")
    row, col = Sgrid.map_to_grid(-9000000., 9000000.)
    assert_almost_equals(row, -0.5, places=precision6)
    assert_almost_equals(col, -0.5, places=precision6)
    Tgrid = Ease2Transform("EASE2_T25km")
    row, col = Tgrid.map_to_grid(-17367530.44, 6756820.2)
    assert_almost_equals(row, -0.5, places=precision6)
    assert_almost_equals(col, -0.5, places=precision6)


def test_origin_Ease2Transform_geographic_to_grid():
    Ngrid = Ease2Transform("EASE2_N25km")
    row, col = Ngrid.geographic_to_grid(90., 0.)
    assert_almost_equals(row, 359.5, places=precision6)
    assert_almost_equals(col, 359.5, places=precision6)
    Sgrid = Ease2Transform("EASE2_S25km")
    row, col = Sgrid.geographic_to_grid(-90., 0.)
    assert_almost_equals(row, 359.5, places=precision4)
    assert_almost_equals(col, 359.5, places=precision4)
    Tgrid = Ease2Transform("EASE2_T25km")
    row, col = Tgrid.geographic_to_grid(0., 0.)
    assert_almost_equals(row, 269.5, places=precision6)
    assert_almost_equals(col, 693.5, places=precision6)


def test_UL_Ease2Transform_geographic_to_grid():
    Ngrid = Ease2Transform("EASE2_N25km")
    row, col = Ngrid.geographic_to_grid(-84.634050, -135.)
    assert_almost_equals(row, -0.5, places=precision6)
    assert_almost_equals(col, -0.5, places=precision6)
    Sgrid = Ease2Transform("EASE2_S25km")
    row, col = Sgrid.geographic_to_grid(84.634050, -45.)
    assert_almost_equals(row, -0.5, places=precision6)
    assert_almost_equals(col, -0.5, places=precision6)
    Tgrid = Ease2Transform("EASE2_T25km")
    row, col = Tgrid.geographic_to_grid(67.057541, -180.)
    assert_almost_equals(row, -0.5, places=precision5)
    assert_almost_equals(col, -0.5, places=precision5)
