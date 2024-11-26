# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.11.0] - 2024-11-26

+ Correct elements to camelCase for daily forecasts.
+ Add option to convert numeric significant weather code to string description

## [0.10.0] - 2024-11-17

+ Modernise packaging and build tooling and infrastructure.
+ Migrate to use new MetOffice DataHub. This required many changes, for more
  details see the 'migration' page of the documentation.

## [0.9.9] - 2024-02-09

+ Update versioneer
+ Add pythons 3.9, 3.10, 3.11, 3.12 to tests and setup.py.
+ Remove support for python < 3.8
+ Remove deprecated `new_old` and `future_old` functions.
+ Add `__str__` functions to `Timestep`, `Element`, `Day`, `Site`
+ Add element to `Forecast` to track if forecast is daily or 3 hourly
+ Change `id` variable in `Forecast`, `Observation`, `Site` to `location_id`.
+ Change `id` variable in `Element` to `field_code`.

## [0.9.8] - 2020-07-03

+ Remove f-string in test

## [0.9.7] - 2020-07-03

+ Bugfix for `get_observation_sites`

## [0.9.6] - 2020-05-05

+ Require arguments to `get_nearest_forecast_site` and `get_nearest_observation_site`.
+ Add python 3.8 to tests and setup.py

## [0.9.5] - 2019-10-01

+ Remove support for Python 3.4.

## [0.9.4] - 2019-09-10

+ Fix to url case in `travis.yml` to enable releases.

## [0.9.3] - 2019-09-10

+ Update README.md and travis.yml due to change in ownership.

## [0.9.2] - 2019-07-26

+ Raise an error if data for the requested location is not provided from the datapoint API.

## [0.9.1] - 2019-05-21

+ Remove stray print statement

## [0.9.0] - 2019-05-18

+ Explicitly state the use of semantic versioning in `README.md`.
+ Add `elements()` function to `Timestep`.
+ Remove night/day indication from weather codes which have them.
+ Change the logic used to calculate the closest timestep to a datetime. The closest timestep to the datetime is now used. Add a new function, `Forecast.at_datetime(target)` to do this. `Forecast.now()` has been changed to use this new function. The old behaviour is deprecated and available using `Forecast.now_old()`. `Forecast.future()` has been changed to use this new function. The old behaviour is deprecated and available using `Forecast.future_old()`.
+ Check if keys are returned from datapoint api in `Manager.py`. Do not attempt to read the values from the dict if they are not there.

## [0.8.0] - 2019-04-05

+ Retry the connection to datapoint if it fails (up to 10 times).
+ Use versioneer to set version number from git tag.
+ Fix failure to return forecast at midnight.
+ Add changelog.

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
