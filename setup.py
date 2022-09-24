# -*- coding: utf-8 -*-

import os
import codecs

from setuptools import setup
from setuptools import find_packages

install_requires = [
    'setuptools',
    'six',
    'Jinja2',
]


def read(*rnames):
    return codecs.open(os.path.join(os.path.dirname(__file__), *rnames), 'r', 'utf-8').read()


setup(name='mr.bob',
      version='1.0.0',
      description='Bob renders directory structure templates',
      long_description=read('README.rst') + '\n' + read('HISTORY.rst'),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Programming Language :: Python",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
      ],
      keywords="template skeleton",
      author='Domen Kozar, Tom Lazar',
      author_email='',
      url='https://github.com/domenkozar/mr.bob.git',
      license='BSD',
      packages=find_packages(),
      install_requires=install_requires,
      extras_require={
          'test': [
              'nose2',
              'coverage',
              'flake8',
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
