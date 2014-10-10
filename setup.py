#!/usr/bin/env python

from distutils.core import setup

setup(name='datapoint',
      version='0.2',
      install_requires=[
          "requests >= 2.3.0",
      ],
      description='Python interface to the Met Office\'s Datapoint API',
      author='Jacob Tomlinson',
      author_email='jacob@jacobtomlinson.co.uk',
      url='https://pypi.python.org/pypi/datapoint',
      packages=['datapoint'],
     )
