'''Module for using the burin matplotlib style.
'''

import os

import matplotlib.pyplot as plt

import burin


def use(style=None):
    '''Replacement for `matplotlib.style.use`, but if no style is provided will
       use burin default style.
    '''
    if style is None:
        style = os.path.join(burin.__path__[0], 'stylelib', 'burin.mplstyle')
    plt.style.use(style)
