#!/usr/bin/env python

from setuptools import setup
import versioneer

setup(name='datapoint',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      install_requires=[
          "requests >= 2.20.0",
          "appdirs",
          "pytz",
      ],
      description='Python interface to the Met Office\'s Datapoint API',
      long_description_content_type='text/x-rst',
      long_description='''
Datapoint for Python
--------------------

*A Python module for accessing weather data via the Met
Office's open data API known as
`Datapoint`.*

**Disclaimer: This module is in no way part of the datapoint
project/service. This module is intended to simplify the use of
Datapoint for small Python projects (e.g school projects). No support
for this module is provided by the Met Office and may break as the
Datapoint service grows/evolves. The author will make reasonable efforts
to keep it up to date and fully featured.**

Changelog
---------

+ Explicitly state the use of semantic versioning in `README.md`.
+ Add `elements()` function to `Timestep`.
+ Remove night/day indication from weather codes which have them.
+ Change the logic used to calculate the closest timestep to a datetime. The closest timestep to the datetime is now used. Add a new function, `Forecast.at_datetime(target)` to do this. `Forecast.now()` has been changed to use this new function. The old behaviour is deprecated and available using `Forecast.now_old()`. `Forecast.future()` has been changed to use this new function. The old behaviour is deprecated and available using `Forecast.future_old()`.
+ Check if keys are returned from datapoint api in `Manager.py`. Do not attempt to read the values from the dict if they are not there.


Installation
------------

.. code:: bash

    $ pip install datapoint

You will also require a `Datapoint API`
key from http://www.metoffice.gov.uk/datapoint/API.

Features
--------

-  List forecast sites
-  Get nearest forecast site from latitiude and longitude
-  Get the following 5 day forecast types for any site
-  Daily (Two timesteps, midday and midnight UTC)
-  3 hourly (Eight timesteps, every 3 hours starting at midnight UTC)
-  Get observation sites
-  Get observations for any site

Contributing changes
--------------------

Please feel free to submit issues and pull requests.

License
-------

GPLv3.
''',
      author='Jacob Tomlinson',
      author_email='jacob@jacobtomlinson.co.uk',
      maintainer='Jacob Tomlinson',
      maintainer_email='jacob@jacobtomlinson.co.uk',
      url='https://github.com/jacobtomlinson/datapoint-python',
      license='GPLv3',
      packages=['datapoint', 'datapoint.regions'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ]
     )
