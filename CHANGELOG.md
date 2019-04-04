# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

+ Use versioneer to set version number from git tag.
+ Retry the connection to datapoint if it fails (up to 10 times).
+ Fix failure to return forecast at midnight.

## [0.7.0] - 2019-02-19

+ Check that data is provided in tests.
+ Set weather element of `timestep` to 'not reported' if data is not provided.
+ Update examples to use `get_nearest_forecast_site` function.
+ Rename `get_all_sites()` to `get_forecast_sites()` and `get_nearest_site()` to `get_nearest_forecast_site()`.
+ Limit observations to sites within 20 km of the nearest observation site.
+ Require that the nearest location is within 30 km of the requested location.
+ Show the available sites on maps in the documentation.
+ Use a haversine function to calculate the distance between coordinates.
+ Use setuptools in `setup.py`.
+ Fix bug where site attributes were assigned incorrectly.
+ Use sphinx to generate documentation.
+ Fix bug where longitude or latitude values of 0 returned false in `get_nearest_site()`.

## [0.6.1] - 2019-01-26

+ Remove stray print statements.

## [0.6.0] - 2019-01-26

+ Remove support for python 2 and python 3.3.

## [0.5.1] - 2019-01-26

+ Correct wrong version number.

## [0.5.0] - 2019-01-26

+ Fix latitude and longitude in `manager_test.py`.
+ Add support for observations.
+ Swap the order of latitude and longitude in function calls.
+ Add a timeout of 1 second to the API call.
+ Fix error which set sites to `None`.
+ Fix documentation build.
+ Use python 3 syntax in examples.
+ Fix bug where `forecast.now()` always returned `None`.
+ Change print statements in `Manager.py` and `Forecast.py` to python 3 style.
+ Fix bug where no data was returned for about an hour after midnight.
+ Add `forecast.future()` function.
+ Add support for python 3.6.

## [0.4.3] - 2017-01-19

+ Use a custom error when datapoint call fails.

## [0.4.2] - 2017-01-18

+ Only send python 3.5 to Travis.

## [0.4.1] - 2017-01-04

+ Update tests.
+ Fix bug with `forecast.now()`.
+ Implement text forecast.

## [0.4.0] - 2016-06-06

+ Add python 3 support.

## [0.3.0] - 2016-01-06

+ Use python datetime for dates and times.
+ Add instructions for installing from master using pip.

## [0.2.2] - 2014-10-24

+ Add examples
+ Use readthedocs.
+ Add error when no data is returned.
+ Cache site requests for an hour.

## [0.2.1] - 2014-10-17

+ Test string to int conversion.

## [0.2] - 2014-10-10

+ Use travis
+ Add concept of API key profiles.
+ Fix type casting.
+ Add `forecast.now()` function.

## [0.1] - 2014-07-16

+ Initial commit and license.
