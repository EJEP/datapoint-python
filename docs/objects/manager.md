# Manager

####Attributes

<table>
<tr>
<td><b>attribute</b></td>
<td><b>type</b></td>
</tr>
<tr>
<td><b>api_key</b></td>
<td>string</td>
</tr>
<tr>
<td><b>call_response</b></td>
<td>dict</td>
</tr>
<tr>
<td><b>sites_last_update</b></td>
<td>float</td>
</tr>
<tr>
<td><b>sites_last_request</b></td>
<td>list of Site objects</td>
</tr>
<tr>
<td><b>sites_update_time</b></td>
<td>int</td>
</tr>
</table>

####Methods

#####get_all_sites()
Returns a list of all available sites.<br/>
returns: list of Site objects

#####get_nearest_site(longitude=False, latitude=False)
Returns the nearest Site object to the specified coordinates.<br/>
param longitude: int or float<br/>
param latitude: int or float<br/>
returns: Site

#####get_forecast_for_site(site_id, frequency="daily"):
Get a forecast for the provided site.<br/>
A frequency of "daily" will return two timesteps:
"Day" and "Night".<br/>
A frequency of "3hourly" will return 8 timesteps:
0, 180, 360 ... 1260 (minutes since midnight UTC)<br/>
param site_id: string or unicode<br/>
param frequency: string ("daily" or "3hourly")<br/>
returns: Forecast

