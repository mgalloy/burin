import burin


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


if __name__ == '__main__':
    temp = 5.0
    functions = [example_ctemp, example_ftemp]
    units = ['C', 'F']
    print 'Example temperature conversions'
    for f in functions:
        for u in units:
            print '%5.1f %s -> %5.1f %s' % (temp, f.units, f(temp, units=u), u)

    d = 1.0
    functions = [example_mdistance, example_ftdistance]
    units = ['m', 'ft']
    print 'Example distance conversions'
    for f in functions:
        for u in units:
            print '%6.2f %-2s -> %4.2f %-2s' % (d, f.units, f(d, units=u), u)