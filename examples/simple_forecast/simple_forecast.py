#!/usr/bin/env python
"""
This example will print out a simple forecast for the next 5 days.
It will allow us to explore the day, timestep and element objects.
"""

import datetime

import datapoint

# Create datapoint connection
manager = datapoint.Manager(
    api_key="api key goes here"
)


forecast = manager.get_forecast(51.500728, -0.124626, frequency="hourly")

# Loop through timesteps and print information
for timestep in forecast.timesteps:
    print(timestep["time"])
    print(timestep["significantWeatherCode"]["value"])
    print(
        "{temp} {temp_units}".format(
            temp=timestep["screenTemperature"]["value"],
            temp_units=timestep["screenTemperature"]["unit_symbol"],
        )
    )

print(forecast.now())

print(forecast.at_datetime(datetime.datetime(2024, 2, 11, 14, 0)))
