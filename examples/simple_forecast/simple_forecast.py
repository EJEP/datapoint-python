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
