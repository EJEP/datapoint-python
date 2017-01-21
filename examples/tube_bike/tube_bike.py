#!/usr/bin/env python
"""
This one's for Londoners. Get the weather for home and work and get the tube status
for your usual line. Then use that information to decide whether you're better off
cycling or catching the tube.
"""

import datapoint
import tubestatus

# Create datapoint connection
conn = datapoint.Manager(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")

# Get nearest site to my house and to work
my_house = conn.get_nearest_site(51.5016730, 0.0057500)
work = conn.get_nearest_site(51.5031650, -0.1123050)

# Get a forecast for my house and work
my_house_forecast = conn.get_forecast_for_site(my_house.id, "3hourly")
work_forecast = conn.get_forecast_for_site(work.id, "3hourly")

# Get the current timestep for both locations
my_house_now = my_house_forecast.now()
work_now = work_forecast.now()

# Create a tube status connection
current_status = tubestatus.Status()

# Get the status of the Waterloo and City line
waterloo_status = current_status.get_status('Waterloo and City')

# Check whether there are any problems with rain or the tube
if (my_house_now.precipitation.value < 40 and \
        work_now.precipitation.value < 40 and \
        waterloo_status.description == "Good Service"):

    print "Rain is unlikely and tube service is good, the decision is yours."

# If it is going to rain then suggest the tube
elif ((my_house_now.precipitation.value >= 40 or \
        work_now.precipitation.value >= 40) and \
        waterloo_status.description == "Good Service"):

    print "Looks like rain, better get the tube"

# If the tube isn't running then suggest cycling
elif (my_house_now.precipitation.value < 40 and \
        work_now.precipitation.value < 40 and \
        waterloo_status.description != "Good Service"):

    print "Bad service on the tube, cycling it is!"

# Else if both are bad then suggest cycling in the rain
else:
    print "The tube has poor service so you'll have to cycle, but it's raining so take your waterproofs."
