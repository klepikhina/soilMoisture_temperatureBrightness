#!/usr/bin/env python
from __future__ import print_function

import matplotlib
matplotlib.use('AGG')

import matplotlib.pyplot as plt  # noqa

from netCDF4 import Dataset   # noqa
import numpy as np   # noqa
import os   # noqa
from osgeo import gdal, osr   # noqa
import re   # noqa
import sys   # noqa


def make_cetb_png(cetb_filename, var_name="TB", verbose=False):
    """
    cetbtools.inspector.make_cetb_png(cetb_filename, var_name="TB", verbose=False)

    Extracts the var_name Dataset from cetb_filename and makes a png image.
    The long_name of the extracted var_name will be used to make a suffix with
    cetb_filename.long_name.png

    Parameters:
       cetb_filename : CETB .nc filename
       var_name : variable name to extract, one of:
                  TB (default), TB_time, TB_std_dev, TB_num_samples,
                  Incidence_angle
       verbose : boolean controls verbose output to stderr (default False)

    Example:
    from cetbtools.inspector import make_cetb_png
    filename = "EASE2_N25km.F13_SSMI.2003001.37H.E.GRD.CSU.v0.1.nc"
    make_cetb_png( filename )

    will extract the data and create the png file
    "EASE2_N25km.F13_SSMI.2003001.37H.E.GRD.CSU.v0.1.nc.GRD_TB.png"

    """
    my_name = __name__ + ":" + sys._getframe().f_code.co_name

    # Read the requested variable and eliminate the time dimension
    try:
        f = Dataset(cetb_filename, 'r', 'NETCDF4')
    except RuntimeError:
        print("%s : Error opening %s" % (my_name, cetb_filename),
              file=sys.stderr)
        raise

    resolution_match = re.search('EASE2_.(.+)km$', f.variables['crs'].long_name)
    assert resolution_match is not None
    resolution = resolution_match.group(1)

    try:
        data = f.variables[var_name][:]
    except KeyError:
        print("%s : No variable %s in file %s"
              % (my_name, var_name, cetb_filename),
              file=sys.stderr)
        raise

    times, rows, cols = np.shape(data)
    data = data.reshape(rows, cols)

    # Downsample 3.125km data

    if resolution == '3.125':
        data = data[::2, ::2]

    # Make the legend label and output filename
    # from the variable's long_name
    label = f.variables[var_name].long_name
    label_with_underscores = re.sub(r' ', r'_', label)

    # Figure out ranges and fill_values for scaling
    valid_range = f.variables[var_name].valid_range
    if "packing_convention" in dir(f.variables[var_name]):
        if verbose:
            print("\n%s : %s data are packed..." % (my_name, var_name),
                  file=sys.stderr)
        add_offset = f.variables[var_name].add_offset
        scale_factor = f.variables[var_name].scale_factor
        valid_range = valid_range * scale_factor + add_offset

    valid_data = data[(valid_range[0] <= data) & (data <= valid_range[1])]
    valid_data_min = np.amin(valid_data)
    valid_data_max = np.amax(valid_data)

    # Some of the valid ranges are a little generous
    # so adjust them to make the images more meaningful
    # We might consider adding command-line parameters to
    # fine-tune these at will, and to control what range is
    # actually displayed
    if "TB" == var_name:
        valid_range[0] = 100.0
    elif "TB_num_samples" == var_name:
        valid_range[1] = valid_data_max
    elif "Incidence_angle" == var_name:
        valid_range = [valid_data_min, valid_data_max]
    elif "TB_std_dev" == var_name:
        valid_range = [valid_data_min, 10.]
    elif "TB_time" == var_name:
        mins_per_day = 60 * 24
        valid_range = [-0.5 * mins_per_day, 1.5 * mins_per_day]

    if verbose:
        print("\n%s : valid data range is %s - %s" %
              (my_name, str(valid_data_min), str(valid_data_max)),
              file=sys.stderr)

    # Make the figure
    fig, ax = plt.subplots(1, 1)
    ax.set_title(os.path.basename(cetb_filename))
    plt.imshow(data, cmap=plt.cm.gray,
               vmin=valid_range[0], vmax=valid_range[1],
               interpolation='None')
    plt.axis('off')
    plt.colorbar(shrink=0.35, label=label)
    outfile = cetb_filename + '.' + label_with_underscores + '.png'
    fig.savefig(outfile, dpi=300, bbox_inches='tight')

    # Clear memory for plot and free netCDF file
    plt.clf()
    f.close()

    if verbose:
        print("\n%s : %s png image saved to: %s" %
              (my_name, var_name, outfile),
              file=sys.stderr)

    return(True)


def make_cetb_geotiff(cetb_filename, var_name="TB", verbose=False):
    """
    cetbtools.inspector.make_cetb_geotiff(cetb_filename,
                                          var_name="TB", verbose=False)

    Extracts the var_name Dataset from cetb_filename and makes a geotiff image.
    The long_name of the extracted var_name will be used to make a suffix with
    cetb_filename.long_name.tif

    Parameters:
       cetb_filename : CETB .nc filename
       var_name : variable name to extract, one of:
                  TB (default), TB_time, TB_std_dev, TB_num_samples,
                  Incidence_angle
       verbose : boolean controls verbose output to stderr (default False)

    Example:
    from cetbtools.inspector import make_cetb_geotiff
    filename = "EASE2_N25km.F13_SSMI.2003001.37H.E.GRD.CSU.v0.1.nc"
    make_cetb_geotiff( filename )

    will extract the data and create the geotiff file
    "EASE2_N25km.F13_SSMI.2003001.37H.E.GRD.CSU.v0.1.nc.GRD_TB.tif"

    """
    my_name = __name__ + ":" + sys._getframe().f_code.co_name

    # Read the requested variable and eliminate the time dimension
    try:
        f = Dataset(cetb_filename, 'r', 'NETCDF4')
    except RuntimeError:
        print("%s : Error opening %s" % (my_name, cetb_filename),
              file=sys.stderr)
        raise

    try:
        data = f.variables[var_name][:]
    except KeyError:
        print("%s : No variable %s in file %s"
              % (my_name, var_name, cetb_filename),
              file=sys.stderr)
        raise

    times, rows, cols = np.shape(data)
    data = data.reshape(rows, cols)

    if ("f4" == data.dtype):
        gdal_data_type = gdal.GDT_Float32
    elif ("u1" == data.dtype):
        gdal_data_type = gdal.GDT_Byte
    elif ("i2" == data.dtype):
        gdal_data_type = gdal.GDT_Int16
    else:
        print("%s : Unrecognized %s type %s " %
              (my_name, var_name, str(data.dtype)),
              file=sys.stderr)
        raise ValueError

    # Make output filename from the variable's long_name
    label_with_underscores = re.sub(r' ', r'_',
                                    f.variables[var_name].long_name)

    outfilename = cetb_filename + '.' + label_with_underscores + '.tif'
    driver = gdal.GetDriverByName("GTiff")

    dest_ds_options = ['COMPRESS=LZW']
    dest_ds = driver.Create(outfilename, cols, rows, 1, gdal_data_type,
                            dest_ds_options)

    # Initialize the projection information
    # When we can connect to epsg v8.6 or later,
    # we should replace proj.4 strings
    # with epsg codes.  For now, we'll just use the proj.4 strings
    # that are included in the file's crs attribute
    proj = osr.SpatialReference()
    dest_srs = str(f.variables["crs"].proj4text)
    proj.SetFromUserInput(dest_srs)
    dest_ds.SetProjection(proj.ExportToWkt())

    # Initialize the grid information (extent and scale)
    # Thanks to web page at:
    # http://geoexamples.blogspot.com/2012/01/
    # creating-files-in-ogr-and-gdal-with.html
    # The geotransform defines the relation between the
    # raster coordinates x, y and the
    # geographic coordinates, using the following definition:
    # Xgeo = geotransform[0] + Xpixel*geotransform[1] + Yline*geotransform[2]
    # Ygeo = geotransform[3] + Xpixel*geotransform[4] + Yline*geotransform[5]
    # The first and fourth parameters define the origin of the upper left pixel
    # The second and sixth parameters define the pixels size.
    # The third and fifth parameters define the rotation of the raster.
    # Values are meters
    # The UL information is in the file's y/x dimension variable ranges
    map_UL_x = f.variables["x"].valid_range[0]
    map_UL_y = f.variables["y"].valid_range[1]

    # Get the projection scale by subtracting the first and second x and y
    # coordinate values
    # This assumes a constant map scale in both dimensions
    scale_x = f.variables["x"][1] - f.variables["x"][0]
    scale_y = f.variables["y"][1] - f.variables["y"][0]

    geotransform = (map_UL_x, scale_x, 0., map_UL_y, 0., scale_y)
    dest_ds.SetGeoTransform(geotransform)
    dest_ds.GetRasterBand(1).WriteArray(data)
    dest_ds = None

    f.close()
    if verbose:
        print("\n%s : %s geotiff image saved to: %s" %
              (my_name, var_name, outfilename),
              file=sys.stderr)

    return(True)
