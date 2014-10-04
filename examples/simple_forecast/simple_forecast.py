#!/usr/bin/env python
"""
This example will print out a simple forecast for the next 5 days.
It will allow is to explore the day, timestep and element objects.
"""

import datapoint

# Create datapoint connection
conn = datapoint.Manager(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")

# Get nearest site and print out its name
site = conn.get_nearest_site(-0.124626, 51.500728)
print site.name

# Get a forecast for the nearest site
forecast = conn.get_forecast_for_site(site.id, "3hourly")

# Loop through days and print date
for day in forecast.days:
    print "\n%s" % day.date

    # Loop through time steps and print out info
    for timestep in day.timesteps:
        print timestep.name
        print timestep.weather.text
        print "%s%s%s" % (timestep.temperature.value,
                          u'\xb0', #Unicode character for degree symbol
                          timestep.temperature.units)

