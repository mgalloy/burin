'''Module to handle unit conversions.
'''


# conversion functions

def identity(x):
    '''Identify conversion. Useful when converting from a unit to itself.
    '''
    return x


def m2ft(d):
    '''Meters to feet conversion.
    '''
    return 3.28084 * d


def ft2m(d):
    '''Feet to meters conversion.
    '''
    return 0.3048 * d


distance_convert_functions = {'m': {'m': identity, 'ft': m2ft},
                              'ft': {'m': ft2m, 'ft': identity}}


def c2f(t):
    '''Celcius to Fahrenheit conversion.
    '''
    return 9.0 * t / 5.0 + 32.0


def f2c(t):
    '''Fahrenheit to Celcius conversion.
    '''
    return 5.0 / 9.0 * (t - 32.0)


temp_convert_functions = {'c': {'c': identity, 'f': c2f},
                          'f': {'c': f2c, 'f': identity}}


def get_convert_function(input_units, output_units):
    '''Helper routine to retrieve the appropriate conversion function given
       the input and output units.
    '''
    if input_units.lower() in distance_convert_functions:
        cf = distance_convert_functions[input_units.lower()]
    elif input_units.lower() in temp_convert_functions:
        cf = temp_convert_functions[input_units.lower()]
    else:
        return identity
    return cf[output_units.lower()]


def convert(units=None):
    '''Decorator to specify the units a function returns.
    '''

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
