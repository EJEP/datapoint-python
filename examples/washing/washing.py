#!/usr/bin/env python
"""
This example will tell us which day would be best to hang out
our washing to dry.

We will loop over the next 5 days and decide whether it is
ok to hang out the washing. Then for the good days we will rank
them and print out the best.
"""

import datapoint
import datetime

# Set thresholds
MAX_WIND = 31 # in mph. We don't want the washing to blow away
MAX_PRECIPITATION = 20 # Max chance of rain we will accept

# Variables for later
best_day = None
best_day_score = 0 # For simplicity the score will be temperature + wind speed

# Create datapoint connection
conn = datapoint.connection()

# Get nearest site and print out its name
site = conn.get_nearest_site(-0.124626, 51.500728)
print site.name

# Get a forecast for the nearest site
forecast = conn.get_forecast_for_site(site.id, "daily")

# Loop through days
for day in forecast.days:

    # Get the 'Day' timestep
    if day.timesteps[0].name == 'Day':
        timestep = day.timesteps[0]
        
        # If precipitation, wind speed and gust are less than their threshold
        if timestep.precipitation.value < MAX_PRECIPITATION and \
           timestep.wind_speed.value < MAX_WIND and \
           timestep.wind_gust.value < MAX_WIND:

            # Calculate the score for this timestep
            timestep_score = timestep.wind_speed.value + timestep.temperature.value

            # If this timestep scores better than the current best replace it
            if timestep_score > best_day_score:
                best_day_score = timestep_score
                best_day = day.date

# If best_day is still None then there are no good days
if best_day == None:
    print "Better use the tumble dryer"

# Otherwise print out the day
else:
    # Convert the date from a string into a datetime object
    best_day_raw = datetime.datetime.strptime(best_day, "%Y-%m-%dZ")
    # Get the day of the week from the datetime object
    best_day_formatted = datetime.datetime.strftime(best_day_raw, "%A")
    print "%s is the best day with a score of %s" % (best_day_formatted, best_day_score)

