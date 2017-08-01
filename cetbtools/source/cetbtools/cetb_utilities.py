#!/usr/bin/env python
import re   # noqa


def _find(pattern, attribute):
    '''Parses the input attribute string using the regex in pattern
    Args:
         pattern - regex to search for
         attribute - string to search
    Results:
         returns the match if found or None
    '''

    pattern = re.compile(pattern)
    match = pattern.search(attribute)

    if match and len(match.groups()) > 0:
        return match.group(1)
    else:
        return None


def duration(attribute):
    '''duration examines the duration variable

    args: input ISO string in the format PddThh:mm:ss.ssZ

    returns: True if the duration variable is 0 or +ve and False otherwise
    '''

    duration = True

    durationday = _find('T(.+):', attribute)
    if (durationday[0] == '-'):
        duration = False

    durationhour = _find(':(.+):', attribute)
    if (durationhour[0] == '-'):
        duration = False

    return duration


def datetime(attribute):
    '''datetime returns the date and time from an ISOstring

    args: input ISO string in the format yyy-mm-ddThh:mm:ss.ssZ

    returns: date and time by splitting the string at the T and Z
    '''

    datestring = _find('(.+)T', attribute)
    timestring = _find('T(.+)Z', attribute)

    return datestring, timestring


def getattr(fd, attribute_string, pattern):
    '''getattr retrieves the value of the requested attribute from
       the open netCDF file

    args: fd - file descriptor pointing to an open netcdf file
          attribute_string - the attribute to retrieve from the file
          pattern - the pattern to match

    returns:  the value of the attribute requested
    '''

    attribute_value = fd.getncattr(attribute_string)
    if (isinstance(attribute_value, unicode)):
        if (len(pattern) == 0):
            pattern = '(.+)'
        attribute_value = _find(pattern, attribute_value)

    return attribute_value
