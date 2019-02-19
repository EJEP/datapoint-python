#!/usr/bin/env python

from setuptools import setup

setup(name='datapoint',
      version='0.7.0',
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
`Datapoint.*

**Disclaimer: This module is in no way part of the datapoint
project/service. This module is intended to simplify the use of
Datapoint for small Python projects (e.g school projects). No support
for this module is provided by the Met Office and may break as the
Datapoint service grows/evolves. The author will make reasonable efforts
to keep it up to date and fully featured.**

Changelog
---------

- The nearest site is now calculated using the haversine formula. The nearest
      site may change.
- Locations must be within 30km of the nearest forecast site.
- Support for observations from DataPoint added. Locations must be within 20km
      of the nearest observation site.
- Deprecation warning: the following function names have been changed:
      `get_all_sites` to `get_forecast_sites`, `get_nearest_site` to
      `get_nearest_forecast_site`.


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
