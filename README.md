# _DataPoint for Python_
[![PyPi version](https://img.shields.io/pypi/v/datapoint.svg)](https://pypi.python.org/pypi/datapoint/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/datapoint.svg)](https://pypi.python.org/pypi/datapoint/)
[![Build Status](http://img.shields.io/travis/jacobtomlinson/datapoint-python.svg?style=flat)](https://travis-ci.org/jacobtomlinson/datapoint-python)
[![Documentation Status](https://readthedocs.org/projects/datapoint-python/badge/?version=latest)](https://readthedocs.org/projects/datapoint-python/)


_A Python module for accessing weather data via the [Met Office](http://www.metoffice.gov.uk/)'s open data API
known as [DataPoint](http://www.metoffice.gov.uk/datapoint)._

__Disclaimer: This module is in no way part of the DataPoint project/service.
This module is intended to simplify the use of DataPoint for small Python projects (e.g school projects).
No support for this module is provided by the Met Office and may break as the DataPoint service grows/evolves.
The author will make reasonable efforts to keep it up to date and fully featured.__

## Features
 * List forecast sites
 * Get nearest forecast site from latitiude and longitude
 * Get the following 5 day forecast types for any site
  * Daily (Two timesteps, midday and midnight UTC)
  * 3 hourly (Eight timesteps, every 3 hours starting at midnight UTC)

## Installation

```Bash
$ pip install DataPoint
```

You will also require a [DataPoint API key](http://www.metoffice.gov.uk/datapoint/API).

For more installation methods see the [installation guide](http://datapoint-python.readthedocs.org/en/latest/install/).

## Documentation

Detailed documentation for this project is available on [Read the Docs](http://datapoint-python.readthedocs.org/en/latest).

## Example Usage

```Python
import datapoint

# Create connection to DataPoint with your API key
conn = datapoint.connection(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")

# Get the nearest site for my latitude and longitude
site = conn.get_nearest_forecast_site(51.500728, -0.124626)

# Get a forecast for my nearest site with 3 hourly timesteps
forecast = conn.get_forecast_for_site(site.id, "3hourly")

# Get the current timestep from the forecast
current_timestep = forecast.now()

# Print out the site and current weather
print site.name, "-", current_timestep.weather.text

```

Example output
```
London - Heavy rain
```

See [examples directory](https://github.com/jacobtomlinson/datapoint-python/tree/master/examples) for more in depth examples.

## Contributing changes

Please feel free to submit issues and pull requests.

## License

GPLv3
