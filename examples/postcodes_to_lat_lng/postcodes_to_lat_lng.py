#!/usr/bin/env python
"""
A variation on current_weather.py which uses postcodes rather than lon lat.
"""

import postcodes_io_api

import datapoint

# Create datapoint connection
conn = datapoint.Manager(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")


# Get longitude and latitude from postcode
postcodes_conn = postcodes_io_api.Api()
postcode = postcodes_conn.get_postcode("SW1A 2AA")
latitude = postcode["result"]["latitude"]
longitude = postcode["result"]["longitude"]

# Get nearest site and print out its name
site = conn.get_nearest_forecast_site(latitude, longitude)
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
