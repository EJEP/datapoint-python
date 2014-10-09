# _Datapoint for Python_
[![PyPi version](https://pypip.in/v/datapoint/badge.svg?style=flat)](https://pypi.python.org/pypi/datapoint/)
[![PyPi downloads](https://pypip.in/d/datapoint/badge.svg?style=flat)](https://pypi.python.org/pypi/datapoint/)
[![Supported Python versions](https://pypip.in/py_versions/datapoint/badge.svg?style=flat)](https://pypi.python.org/pypi/datapoint/)
[![Development Status](https://pypip.in/status/datapoint/badge.svg?style=flat)](https://pypi.python.org/pypi/datapoint/)
[![License](https://pypip.in/license/datapoint/badge.svg?style=flat)](https://pypi.python.org/pypi/datapoint/)


_A Python module for accessing weather data via the [Met Office](http://www.metoffice.gov.uk/)'s open data API
known as [Datapoint](http://www.metoffice.gov.uk/datapoint)._

__Disclaimer: This module is in no way part of the datapoint project/service.
This module is intended to simplify the use of Datapoint for small Python projects (e.g school projects).
No support for this module is provided by the Met Office and may break as the Datapoint service grows/evolves.
The author will make reasonable efforts to keep it up to date and fully featured.__

## Installation

```Bash
$ pip install datapoint
```

You will also require a [Datapoint API key](http://www.metoffice.gov.uk/datapoint/API).
## Example Usage

```Python
#!/usr/bin/env python

import datapoint

conn = datapoint.Manager(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")

site = conn.get_nearest_site(-0.124626, 51.500728)
print site.name

forecast = conn.get_forecast_for_site(site.id, "3hourly")

for day in forecast.days:
    print "\n%s" % day.date
    for timestep in day.timesteps:
        print timestep.name
        print timestep.weather.text
        print "%s%s%s" % (timestep.temperature.value,
                          u'\xb0', #Unicode character for degree symbol
                          timestep.temperature.units)

```

Example output
```
London

2014-07-16Z
360
Sunny day
16°C
540
Sunny day
22°C
720
Partly cloudy (day)
24°C
900
Cloudy
26°C
1080
Cloudy
25°C
1260
Partly cloudy (night)
23°C

...
```

## Features
 * List forecast sites
 * Get nearest forecast site from longitude and latitiude
 * Get the following 5 day forecast types for any site
  * Daily (Two timesteps, midday and midnight UTC)
  * 3 hourly (Eight timesteps, every 3 hours starting at midnight UTC)

## Contributing changes

Please feel free to submit issues and pull requests.

## License

[MIT Licence](http://opensource.org/licenses/MIT)
