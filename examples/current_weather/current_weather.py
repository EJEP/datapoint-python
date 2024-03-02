#!/usr/bin/env python
"""
This is a simple example which will print out the current weather and
temperature for our location.
"""

import datapoint

# Create datapoint connection
conn = datapoint.Manager(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")

# Get nearest site and print out its name

site = conn.get_nearest_forecast_site(51.500728, -0.124626)
print(site.name)

# Get a forecast for the nearest site
forecast = conn.get_forecast_for_site(site.location_id, "3hourly")

# Get the current timestep using now() and print out some info
now = forecast.now()
print(now.weather.text)
print(
    "%s%s%s"
    % (
        now.temperature.value,
        "\xb0",  # Unicode character for degree symbol
        now.temperature.units,
    )
)
