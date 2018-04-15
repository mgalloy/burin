import os

import burin


def test_epoch_validate():
    d = os.path.dirname(os.path.realpath(__file__))
    epochs_filename = os.path.join(d, 'epochs.cfg')
    spec_filename = os.path.join(d, 'epochs_spec.cfg')
    ep = burin.config.EpochParser(epochs_filename, spec_filename)
    assert(ep.validate())


def test_epoch_get():
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
