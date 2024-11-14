#!/usr/bin/env python
"""
This example checks whether it is due to rain at any point
today and then decides if we need to take an umbrella.
"""

import datetime

import datapoint

# Create umbrella variable to use later
umbrella = False

# Create datapoint connection
manager = datapoint.Manager(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")

# Get a forecast for the nearest site
forecast = manager.get_forecast(51.500728, -0.124626, "hourly")

# Loop through all the timesteps in day 0 (today)
for timestep in forecast.timesteps:
    # Check to see if the chance of rain is more than 20% at any point
    if (
        timestep["probOfPrecipitation"]["value"] > 20
        and timestep["time"].date == datetime.date.now()
    ):
        umbrella = True

# Print out the results
if umbrella is True:
    print("Looks like rain! Better take an umbrella.")
else:
    print("Don't worry you don't need an umbrella today.")
