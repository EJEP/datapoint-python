#!/usr/bin/env python
"""
This is a simple example which will print out the current weather and
temperature for our location.
"""

import datapoint

# Create datapoint connection
manager = datapoint.Manager(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")

# Get a forecast for the nearest location
forecast = manager.get_forecast(51.500728, -0.124626, "hourly")

# Get the current timestep using now() and print out some info
now = forecast.now()
print(now["significantWeatherCode"])
print(f"{now['screenTemperature']['value']} {now['screenTemperature']['unit_symbol']}")
