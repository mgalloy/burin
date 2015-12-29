metric  = 1
english = 2


def c2f(t):
    return 9.0 * t / 5.0 + 32.0


def convert(convert_function=lambda x: x):
    def decorate(func):
        def f(x, units=1):
            return func(x) if units == metric else convert_function(func(x))
        return f
    return decorate


@convert(convert_function=c2f)
def compute_temp(t):
    return 2.0 * t


if __name__ == '__main__':
    print compute_temp(5.0, units=metric)
    print compute_temp(5.0, units=english)
