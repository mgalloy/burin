import burin

# simple decorated routines that will be used by the unit tests

@burin.units.convert(units='C')
def example_ctemp(t):
    '''Example function that natively returns temperatures in C.'''
    return t


@burin.units.convert(units='F')
def example_ftemp(t):
    '''Example function that natively returns temperatures in F.'''
    return t


@burin.units.convert(units='m')
def example_mdistance(d):
    return d


@burin.units.convert(units='ft')
def example_ftdistance(d):
    return d


def test_ctemp_to_c():
    temps = [0.0, 1.0, 5.0, -1.0]
    for t in temps:
        assert example_ctemp(t) == t, 'wrong value for %f' % t
    for t in temps:
        assert example_ctemp(t, units='C') == t, 'wrong value for %f' % t


def test_ctemp_to_f():
    standards = [(0.0, 32.0), (100.0, 212.0)]
    for s in standards:
        assert example_ctemp(s[0], units='F') == s[1], 'error converting %0.1f C to F' % s[0]


def test_ftemp_to_f():
    temps = [0.0, 1.0, 5.0, -1.0]
    for t in temps:
        assert example_ftemp(t) == t, 'wrong value for %f' % t
    for t in temps:
        assert example_ftemp(t, units='F') == t, 'wrong value for %f' % t


def test_ftemp_to_c():
    standards = [(32.0, 0.0), (212.0, 100.0)]
    for s in standards:
        assert example_ftemp(s[0], units='C') == s[1], 'error converting %0.1f F to C' % s[0]


def test_mdistance_to_m():
    distances = [0.0, 1.0, 5.0, -1.0]
    for d in distances:
        assert example_mdistance(d) == d, 'wrong value for %f' % d
    for d in distances:
        assert example_mdistance(d, 'm') == d, 'wrong value for %f' % d


def test_mdistance_to_ft():
    standards = [(0.0, 0.0), (1.0, 3.28084), (-1.0, -3.28084)]
    for s in standards:
        assert example_mdistance(s[0], units='ft') == s[1], 'error converting %0.1f m to ft' % s[0]


def test_ftdistance_to_ft():
    distances = [0.0, 1.0, 5.0, -1.0]
    for d in distances:
        assert example_ftdistance(d) == d, 'wrong value for %f' % d
    for d in distances:
        assert example_ftdistance(d, 'ft') == d, 'wrong value for %f' % d


def test_ftdistance_to_m():
    standards = [(0.0, 0.0), (1.0, 0.3048), (-1.0, -0.3048)]
    for s in standards:
        assert example_ftdistance(s[0], units='m') == s[1], 'error converting %0.1f ft to m' % s[0]
