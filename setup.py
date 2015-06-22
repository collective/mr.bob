# -*- coding: utf-8 -*-

import os
import sys
import codecs

from setuptools import setup
from setuptools import find_packages

install_requires = [
    'setuptools',
    'six>=1.2.0',  # 1.1.0 release doesn't have six.moves.input
]

if (3,) < sys.version_info < (3, 3):
    # Jinja 2.7 drops Python 3.2 compat.
    install_requires.append('Jinja2>=2.5.0,<2.7dev')
else:
    install_requires.append('Jinja2>=2.5.0')

try:
    import importlib  # NOQA
except ImportError:
    install_requires.append('importlib')

try:
    from collections import OrderedDict  # NOQA
except ImportError:
    install_requires.append('ordereddict')

try:
    import argparse  # NOQA
except ImportError:
    install_requires.append('argparse')


def read(*rnames):
    return codecs.open(os.path.join(os.path.dirname(__file__), *rnames), 'r', 'utf-8').read()


setup(name='mr.bob',
      version='0.2.dev0',
      description='Bob renders directory structure templates',
      long_description=read('README.rst') + '\n' + read('HISTORY.rst'),
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
      ],
      author='Domen Kozar, Tom Lazar',
      author_email='',
      url='https://github.com/iElectric/mr.bob.git',
      license='BSD',
      packages=find_packages(),
      install_requires=install_requires,
      extras_require={
          'test': [
              'nose',
              'coverage<3.6dev',
              'flake8>2.0',
              'mock',
          ],
          'development': [
              'zest.releaser',
              'Sphinx',
          ],
      },
      entry_points="""
      [console_scripts]
      mrbob = mrbob.cli:main
      """,
      include_package_data=True,
      zip_safe=False,
      )
