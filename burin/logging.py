'''Module containing helper functions for logging.
'''

import glob
import logging
import os
import re


def rotate_logs(basename, max_version=None):
    '''Rotate logs to allow a new log to be written as basename. If
       max_version is given, delete logs with given basename and versions
       beyond the max_version.

       Note: rotating or pruning done if basename doesn't already exist.

       basename : str
         log base filename, i.e., without a ".x"
       max_version : int
         largest allowable version, set to 0 not keep any versions
    '''

    # nothing to do if the basename doesn't already exist
    if not os.path.isfile(basename):
        return

    files = glob.glob(f'{basename}.*')
    n = len(basename)

    versions = [int(f[n + 1:]) for f in files if f[n + 1:].isdigit()]
    sorted_versions = sorted(versions, reverse=True)

    for v in sorted_versions:
        if max_version is not None and v >= max_version:
            os.remove(f'{basename}.{v}')
        else:
            os.rename(f'{basename}.{v}', f'{basename}.{v+1}')

    # move original if space
    if max_version is not None and max_version > 0:
        os.rename(basename, f'{basename}.1')
    else:
        os.remove(basename)


def get_level(level_name):
    levels = {'CRITICAL': logging.CRITICAL,
              'ERROR': logging.ERROR,
              'WARNING': logging.WARNING,
              'INFO': logging.INFO,
              'DEBUG': logging.DEBUG}
    return levels[level_name.upper()]
