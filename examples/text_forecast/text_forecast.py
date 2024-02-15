#!/usr/bin/env python
"""
This example will print out the 30 day text forecast for a region of the UK.
"""

import datapoint

# Create datapoint connection
conn = datapoint.Manager(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")

# Get all regions and print out their details
regions = conn.regions.get_all_regions()
for region in regions:
    print((region.name, region.location_id, region.region))

# Get all forecasts for a specific region
my_region = regions[0]
forecast = conn.regions.get_raw_forecast(my_region.location_id)["RegionalFcst"]

# Print the forecast details
print("Forecast for {} (issued at {}):".format(my_region.name, forecast["issuedAt"]))

sections = forecast["FcstPeriods"]["Period"]
for section in forecast["FcstPeriods"]["Period"]:
    paragraph = []
    content = section["Paragraph"]

    # Some paragraphs have multiple sections
    if isinstance(content, dict):
        paragraph.append(content)
    else:
        paragraph = content

    for line in paragraph:
        print("{}\n{}\n".format(line["title"], line["$"]))
