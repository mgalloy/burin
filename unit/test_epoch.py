import datetime
import os

import pytest

import burin


def test_epoch_validate():
    '''Test validating an epoch file.'''
    d = os.path.dirname(os.path.realpath(__file__))
    epochs_filename = os.path.join(d, 'epochs.cfg')
    spec_filename = os.path.join(d, 'epochs_spec.cfg')
    ep = burin.config.EpochParser(epochs_filename, spec_filename)
    assert(ep.is_valid())


def test_epoch_get():
    '''Test getting epoch values.'''
    d = os.path.dirname(os.path.realpath(__file__))
    epochs_filename = os.path.join(d, 'epochs.cfg')
    spec_filename = os.path.join(d, 'epochs_spec.cfg')
    ep = burin.config.EpochParser(epochs_filename, spec_filename)

    ep.date = '20171231'
    assert(ep.get('cal_version') == 0)
    assert(ep.get('nx') == 1024)

    ep.date = '20180101'
    assert(ep.get('cal_version') == 1)
    assert(ep.get('nx') == 1024)

    ep.date = '20180101.080001'
    assert(ep.get('cal_version') == 2)
    assert(ep.get('nx') == 1024)

    ep.date = '20180101.080001'
    assert(ep.get('cal_version') == 2)
    assert(ep.get('nx') == 1024)

    ep.date = datetime.datetime(2018, 1, 1, hour=8, minute=0, second=1)
    assert(ep.get('cal_version') == 2)
    assert(ep.get('nx') == 1024)

    assert(ep.get('cal_version', date='20180101.080001') == 2)
    assert(ep.get('nx', date='20180101.080001') == 1024)


def test_epoch_get_nodate():
    d = os.path.dirname(os.path.realpath(__file__))
    epochs_filename = os.path.join(d, 'epochs.cfg')
    spec_filename = os.path.join(d, 'epochs_spec.cfg')
    ep = burin.config.EpochParser(epochs_filename, spec_filename)

    with pytest.raises(KeyError):
        assert(ep.get('cal_version') == 0)
