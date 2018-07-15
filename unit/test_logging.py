import glob
import logging
import os
import pytest
import tempfile

import burin.logging


@pytest.fixture()
def create_testdir(request):
    '''Create and remove a test directory for each of the rotate_logs tests.'''
    dirname = os.path.join(tempfile.gettempdir(), 'burin.logging')
    os.mkdir(dirname)
    def remove_testdir():
        os.rmdir(dirname)
    request.addfinalizer(remove_testdir)


def _make_fullpath(basenames):
    '''Expand a list of basenames to fullpaths in a temporary directory.'''
    return [os.path.join(tempfile.gettempdir(), 'burin.logging', bname)
            for bname in basenames]


def _make_files(filenames):
    '''Touch a list of filenames.'''
    for fname in filenames:
        # dirname = os.path.dirname(fname)
        # if not os.path.isdir(dirname):
        #     os.mkdir(dirname)
        with open(fname, 'w'):
            os.utime(fname)


def _clean_files(filenames):
    '''Remove a list of filenames.'''
    for f in filenames:
        os.remove(f)


def test_rotate(create_testdir):
    '''Test on a normal rotate.'''
    basenames = ['mike.log', 'mike.log.1', 'mike.log.2']
    filenames = _make_fullpath(basenames)
    _make_files(filenames)

    burin.logging.rotate_logs(filenames[0])

    standards = ['mike.log.1', 'mike.log.2', 'mike.log.3']
    standard_filenames = _make_fullpath(standards)

    _clean_files(standard_filenames)
    remaining = glob.glob(os.path.join(os.path.dirname(filenames[0]), '*'))
    assert len(remaining) == 0, 'extra log files'


def test_max_version(create_testdir):
    '''Test on a rotate with a max_version.'''
    basenames = ['mike.log', 'mike.log.1', 'mike.log.2', 'mike.log.3']
    filenames = _make_fullpath(basenames)
    _make_files(filenames)

    burin.logging.rotate_logs(filenames[0], max_version=3)

    standards = ['mike.log.1', 'mike.log.2', 'mike.log.3']
    standard_filenames = _make_fullpath(standards)

    _clean_files(standard_filenames)
    remaining = glob.glob(os.path.join(os.path.dirname(filenames[0]), '*'))
    assert len(remaining) == 0, 'extra log files'


def _test_max_version_0(create_testdir):
    '''Test on a rotate with a max_version=0.'''
    basenames = ['mike.log', 'mike.log.1', 'mike.log.2', 'mike.log.3']
    filenames = _make_fullpath(basenames)
    _make_files(filenames)

    burin.logging.rotate_logs(filenames[0], max_version=0)

    remaining = glob.glob(os.path.join(os.path.dirname(filenames[0]), '*'))
    assert len(remaining) == 0, 'extra log files'


def test_no_basename(create_testdir):
    '''Test on a rotate when the basename is not present.'''
    bname = _make_fullpath(['mike.log'])
    basenames = ['mike.log.1', 'mike.log.2', 'mike.log.3']
    filenames = _make_fullpath(basenames)
    _make_files(filenames)

    burin.logging.rotate_logs(bname[0], max_version=3)

    standards = ['mike.log.1', 'mike.log.2', 'mike.log.3']
    standard_filenames = _make_fullpath(standards)

    _clean_files(standard_filenames)
    remaining = glob.glob(os.path.join(os.path.dirname(filenames[0]), '*'))
    assert len(remaining) == 0, 'extra log files'


def test_get_level():
    levels = [('debug', logging.DEBUG),
              ('info', logging.INFO),
              ('warn', logging.WARN),
              ('warning', logging.WARN),
              ('error', logging.ERROR),
              ('critical', logging.CRITICAL)]
    for name, level in levels:
        assert burin.logging.get_level(name) == level

    try:
        bad_level = burin.logging.get_level('bad_name')
    except KeyError:
        # this is success
        pass