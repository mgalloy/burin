
# conversion functions

def identity(x):
    return x


def m2ft(d):
    return 3.28084 * d

def ft2m(d):
    return 0.3048 * d

distance_convert_functions = {'m': {'m': identity, 'ft': m2ft},
                              'ft': {'m': ft2m, 'ft': identity}}

def c2f(t):
    return 9.0 * t / 5.0 + 32.0

def f2c(t):
    return 5.0 / 9.0 * (t - 32.0)

temp_convert_functions = {'c': {'c': identity, 'f': c2f},
                          'f': {'c': f2c, 'f': identity}}


def get_convert_function(input_units, output_units):
    if input_units.lower() in distance_convert_functions:
        cf = distance_convert_functions[input_units.lower()]
    elif input_units.lower() in temp_convert_functions:
        cf = temp_convert_functions[input_units.lower()]
    else:
        return identity
    return cf[output_units.lower()]


def convert(units=None):
    def decorate(func):
        input_units = units
        def f(x, units=None):
            if units is None:
                cf = identity
            else:
                cf = get_convert_function(input_units, units)
            return cf(func(x))
        f.units = input_units
        return f
    return decorate


@convert(units='C')
def example_ctemp(t):
    '''Example function that natively returns temperatures in C.'''
    return t


@convert(units='F')
def example_ftemp(t):
    '''Example function that natively returns temperatures in F.'''
    return t


@convert(units='m')
def example_mdistance(d):
    return d


@convert(units='ft')
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

