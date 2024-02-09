#!/usr/bin/env python
"""
This example checks whether it is due to rain at any point
today and then decides if we need to take an umbrella.
"""

import datapoint

# Create umbrella variable to use later
umbrella = False

# Create datapoint connection
conn = datapoint.Manager(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")

# Get nearest site and print out its name
site = conn.get_nearest_forecast_site(51.500728, -0.124626)
print(site.name)

# Get a forecast for the nearest site
forecast = conn.get_forecast_for_site(site.location_id, "3hourly")

# Loop through all the timesteps in day 0 (today)
for timestep in forecast.days[0].timesteps:
    # Check to see if the chance of rain is more than 20% at any point
    if timestep.precipitation.value > 20:
        umbrella = True

# Print out the results
if umbrella == True:
    print("Looks like rain! Better take an umbrella.")
else:
    print("Don't worry you don't need an umbrella today.")
