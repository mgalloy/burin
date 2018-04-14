import os

import burin


def test_config_verify():
    d = os.path.dirname(os.path.realpath(__file__))
    good_filename = os.path.join(d, 'good.cfg')

    vconfig = burin.config.VerifiedConfigParser(os.path.join(d, 'spec.cfg'))

    assert(vconfig.verify(os.path.join(d, 'good.cfg')))
    assert(not vconfig.verify(os.path.join(d, 'extra_option.cfg')))
    assert(not vconfig.verify(os.path.join(d, 'extra_section.cfg')))

