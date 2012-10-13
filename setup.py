# -*- coding: utf-8 -*-

import os

from setuptools import setup
from setuptools import find_packages

install_requires = [
    'setuptools',
    'argparse',
    'jinja2',
]

try:
    import importlib
except ImportError:
    install_requires.append('importlib')


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(name='mr.bob',
      version='0.1',
      description='Bob renders directory structure templates',
      long_description=read('README.rst') +
                       read('HISTORY.rst') +
                       read('LICENSE'),
      classifiers=[
          "Programming Language :: Python",
      ],
      #keywords='',
      author='Domen Kozar, Tom Lazar',
      author_email='',
      url='https://github.com/iElectric/mr.bob.git',
      license='BSD',
      packages=find_packages(),
      install_requires=install_requires,
      extras_require={
          'test': [
              'pytest',
              'pytest-cov',
              'unittest2',
              'setuptools-flakes',
              'pep8',
              'pytest',
          ],
          'development': [
              'zest.releaser',
          ],
      },
      entry_points="""
      [console_scripts]
      mrbob = mrbob.cli:main
      """,
      include_package_data=True,
      zip_safe=False,
      )
