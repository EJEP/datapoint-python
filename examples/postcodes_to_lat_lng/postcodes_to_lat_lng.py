#!/usr/bin/env python
"""
A variation on current_weather.py which uses postcodes rather than lon lat.
"""

import postcodes_io_api

import datapoint

# Create datapoint connection
manager = datapoint.Manager(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")


# Get longitude and latitude from postcode
postcodes_conn = postcodes_io_api.Api()
postcode = postcodes_conn.get_postcode("SW1A 2AA")
latitude = postcode["result"]["latitude"]
longitude = postcode["result"]["longitude"]

# Get a forecast for the nearest site
forecast = manager.get_forecast(longitude, latitude, "hourly")

# Get the current timestep using now() and print out some info
now = forecast.now()
print(now["significantWeatherCode"])
print(f"{now['screenTemperature']['value']} {now['screenTemperature']['unit_symbol']}")
