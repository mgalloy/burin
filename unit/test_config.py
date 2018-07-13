import os

import burin


def test_config_validate():
    d = os.path.dirname(os.path.realpath(__file__))
    cp = burin.config.ConfigParser(os.path.join(d, 'spec.cfg'))

    assert(cp.is_valid(os.path.join(d, 'good.cfg')))
    assert(cp.is_valid(os.path.join(d, 'interp.cfg')))
    assert(not cp.is_valid(os.path.join(d, 'missing_option.cfg')))
    assert(not cp.is_valid(os.path.join(d, 'extra_option.cfg')))
    assert(not cp.is_valid(os.path.join(d, 'extra_section.cfg')))


def test_config_typed_get():
    d = os.path.dirname(os.path.realpath(__file__))
    cp = burin.config.ConfigParser(os.path.join(d, 'spec.cfg'))
    cp.read(os.path.join(d, 'good.cfg'))

    basedir = cp.typed_get('logging', 'basedir')
    assert(type(basedir) == str)
    assert(basedir == '/Users/mgalloy/data')

    rotate = cp.typed_get('logging', 'rotate')
    assert(type(rotate) == bool)
    assert(not rotate)

    max_version = cp.typed_get('logging', 'max_version')
    assert(type(max_version) == int)
    assert(max_version == 3)


def test_config_get():
    d = os.path.dirname(os.path.realpath(__file__))
    cp = burin.config.ConfigParser(os.path.join(d, 'spec.cfg'))
    cp.read(os.path.join(d, 'good.cfg'))

    basedir = cp.get('logging', 'basedir')
    assert(basedir == '/Users/mgalloy/data')

    rotate = cp.get('logging', 'rotate')
    assert(rotate == 'NO')

    max_version = cp.get('logging', 'max_version')
    assert(max_version == '3')


def test_config_interp():
    d = os.path.dirname(os.path.realpath(__file__))
    cp = burin.config.ConfigParser(os.path.join(d, 'spec.cfg'))
    cp.read(os.path.join(d, 'interp.cfg'))

    basedir = cp.get('logging', 'basedir')
    assert(basedir == '/Users/mgalloy/data')

    rotate = cp.get('logging', 'rotate')
    assert(rotate == 'NO')

    max_version = cp.get('logging', 'max_version')
    assert(max_version == '3')


def test_config_verified_get_list():
    return
    d = os.path.dirname(os.path.realpath(__file__))
    cp = burin.config.ConfigParser(os.path.join(d, 'spec.cfg'))
    cp.read(os.path.join(d, 'good.cfg'))

    wavelengths = cp.verified_get('level1', 'wavelengths')
    assert(len(wavelengths) == 3)
    assert(wavelengths[0] == '1074')
    assert(wavelengths[1] == '1079')
    assert(wavelengths[2] == '1083')
