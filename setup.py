import os

import numpy
from setuptools import setup, Extension

numpy_include_dir = os.path.join(os.path.dirname(numpy.__file__), 'core', 'include')

flow_module = Extension('flow',
                        sources=['burin/flow.c'],
                        include_dirs=[numpy_include_dir])


def read(fname):
    '''Easy way to read a top-level file such as the README.rst file.
    '''
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='burin',
      version='0.0.1',
      author='mgalloy',
      author_email='mgalloy@gmail.com',
      description='Python library for visualization',
      long_description=read('README.md'),
      packages=['burin'],
      ext_modules=[flow_module],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      test_suite='unit',
      classifiers=[
          'Development Status :: 4 - Beta'
      ],
      install_requires=[
          'matplotlib',
          'numpy',
          'scipy'
      ])
