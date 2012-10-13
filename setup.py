# -*- coding: utf-8 -*-

import os

from setuptools import setup
from setuptools import find_packages


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
      author='',
      author_email='Domen Kozar, Tom Lazar',
      url='https://github.com/iElectric/mr.bob.git',
      license='bsd',
      packages=find_packages(),
      install_requires=[
          'setuptools',
      ],
      extras_require={
          'test': [
              'nose',
              'nose-selecttests',
              'coverage',
              'unittest2',
              'setuptools-flakes',
              'pep8',
          ],
          'development': [
              'zest.releaser',
          ],
      },
      entry_points="""
      """,
      include_package_data=True,
      zip_safe=False,
      )
