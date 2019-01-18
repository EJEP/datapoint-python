#!/usr/bin/env python
"""
A variation on current_weather.py which uses postcodes rather than lon lat.
"""

import datapoint
import postcodes

# Create datapoint connection
conn = datapoint.Manager(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")

# Get longitude and latitude from postcode
pc = postcodes.PostCoder()
result = pc.get('SW1A 2AA')
latitude = result['geo']['lat']
longitude = result['geo']['lng']

# Get nearest site and print out its name
site = conn.get_nearest_site(longitude, latitude)
print(site.name)

# Get a forecast for the nearest site
forecast = conn.get_forecast_for_site(site.id, "3hourly")

# Get the current timestep using now() and print out some info
now = forecast.now()
print(now.weather.text)
print("%s%s%s" % (now.temperature.value,
                  '\xb0', #Unicode character for degree symbol
                  now.temperature.units))
