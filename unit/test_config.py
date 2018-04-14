import os

import burin


def test_config_verify():
    d = os.path.dirname(os.path.realpath(__file__))
    vcp = burin.config.VerifiedConfigParser(os.path.join(d, 'spec.cfg'))

    assert(vcp.verify(os.path.join(d, 'good.cfg')))
    assert(not vcp.verify(os.path.join(d, 'missing_option.cfg')))
    assert(not vcp.verify(os.path.join(d, 'extra_option.cfg')))
    assert(not vcp.verify(os.path.join(d, 'extra_section.cfg')))


def test_config_verified_get():
    d = os.path.dirname(os.path.realpath(__file__))
    vcp = burin.config.VerifiedConfigParser(os.path.join(d, 'spec.cfg'))
    vcp.read(os.path.join(d, 'good.cfg'))

    basedir = vcp.verified_get('logging', 'basedir')
    assert(basedir == '/Users/mgalloy/data')

    rotate = vcp.verified_get('logging', 'rotate')
    assert(rotate == False)

    max_version = vcp.verified_get('logging', 'max_version')
    assert(max_version == 3)


def test_config_verified_get_list():
    return
    d = os.path.dirname(os.path.realpath(__file__))
    vcp = burin.config.VerifiedConfigParser(os.path.join(d, 'spec.cfg'))
    vcp.read(os.path.join(d, 'good.cfg'))

    wavelengths = vcp.verified_get('level1', 'wavelengths')
    assert(len(wavelengths) == 3)
    assert(wavelengths[0] == '1074')
    assert(wavelengths[1] == '1079')
    assert(wavelengths[2] == '1083')
