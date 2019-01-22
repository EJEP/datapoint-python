# Objects

DataPoint for Python makes use of objects for almost everything.
There are 6 different objects which will be returned by the module.

The diagram below shows the main classes used by the library, and how to move between them.

![classes](https://cloud.githubusercontent.com/assets/9357195/4751636/83f178cc-5aa0-11e4-8eb0-a1b9531ed319.png)

## Manager
The object which stores your API key and has methods to access the API.

#### Attributes

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
<tr>
<td><b>observation_sites_last_update</b></td>
<td>float</td>
</tr>
<tr>
<td><b>observation_sites_last_request</b></td>
<td>list of Site objects</td>
</tr>
<tr>
<td><b>observation_sites_update_time</b></td>
<td>int</td>
</tr>
</table>
<br />

#### Methods

##### get_all_sites()
Returns a list of all available sites.<br/>
returns: list of Site objects

##### get_nearest_site(longitude=False, latitude=False)
Returns the nearest Site object to the specified coordinates.<br/>
param longitude: int or float<br/>
param latitude: int or float<br/>
returns: Site

##### get_forecast_for_site(site_id, frequency="daily")
Get a forecast for the provided site.<br/>
A frequency of "daily" will return two timesteps:
"Day" and "Night".<br/>
A frequency of "3hourly" will return 8 timesteps:
0, 180, 360 ... 1260 (minutes since midnight UTC)<br/>
param site_id: string or unicode<br/>
param frequency: string ("daily" or "3hourly")<br/>
returns: Forecast

##### get_observation_sites()
Returns a list of sites for which observations are available.<br/>
returns: list of Site objects

##### get_nearest_observation_site(longitude=False, latitude=False)
Returns the nearest Site object to the specified coordinates.<br/>
param longitude: int or float<br/>
param latitude: int or float<br/>
returns: Site

##### get_observations_for_site(site_id, frequency='hourly')
Get the observations for the provided site.<br/>
Only hourly observations are available, and provide the last 24 hours of data.<br/>
param site_id: string or unicode<br/>
param frequency: string ("daily" or "3hourly")<br/>
returns: Observation



## Site
An object containing details about a specific forecast or observation site.

#### Attributes

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
<td><b>name</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>id</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>elevation</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>latitude</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>longitude</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>nationalPark</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>region</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>unitaryAuthArea</b></td>
<td>unicode</td>
</tr>
</table>
<br />

## Forecast
An object with properties of a single forecast and a list of Day objects.

#### Attributes

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
<td><b>data_date</b></td>
<td>datetime</td>
</tr>
<tr>
<td><b>continent</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>country</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>name</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>longitude</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>latitude</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>id</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>elevation</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>days</b></td>
<td>list of Day objects</td>
</tr>
</table>
<br />

#### Methods

##### now()
Get the current timestep from this forecast<br>
returns: Timestep (or False)

## Observation
An object with the properties of a single observation and a list of Day objects.

#### Attributes

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
<td><b>data_date</b></td>
<td>datetime</td>
</tr>
<tr>
<td><b>continent</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>country</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>name</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>longitude</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>latitude</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>id</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>elevation</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>days</b></td>
<td>list of Day objects</td>
</tr>
</table>
<br/>

#### Methods

##### now()
Get the current timestep from this observation<br>
returns: Timestep

## Day
An object with properties of a single day and a list of Timestep objects.

#### Attributes

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
<td><b>date</b></td>
<td>datetime</td>
</tr>
<tr>
<td><b>timesteps</b></td>
<td>list of Timestep objects</td>
</tr>
</table>
<br />

## Timestep
An object with each forecast property (wind, temp, etc) for a specific time,
in the form of Element objects.

#### Attributes

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
<td><b>name</b></td>
<td>string</td>
</tr>
<tr>
<td><b>date</b></td>
<td>datetime</td>
</tr>
<tr>
<td><b>weather</b></td>
<td>Element</td>
</tr>
<tr>
<td><b>temperature</b></td>
<td>Element</td>
</tr>
<tr>
<td><b>feels_like_temperature</b></td>
<td>Element</td>
</tr>
<tr>
<td><b>wind_speed</b></td>
<td>Element</td>
</tr>
<tr>
<td><b>wind_direction</b></td>
<td>Element</td>
</tr>
<tr>
<td><b>wind_gust</b></td>
<td>Element</td>
</tr>
<tr>
<td><b>visibility</b></td>
<td>Element</td>
</tr>
<tr>
<td><b>uv</b></td>
<td>Element</td>
</tr>
<tr>
<td><b>precipitation</b></td>
<td>Element</td>
</tr>
<tr>
<td><b>humidity</b></td>
<td>Element</td>
</tr>
</table>
<br />

## Element
An object with properties about a specific weather element.

#### Attributes

<table>
<tr>
<td><b>attribute</b></td>
<td><b>type</b></td>
</tr>
<tr>
<td><b>id</b></td>
<td>string</td>
</tr>
<tr>
<td><b>value</b></td>
<td>int</td>
</tr>
<tr>
<td><b>units</b></td>
<td>unicode</td>
</tr>
<tr>
<td><b>text</b></td>
<td>string or None</td>
</tr>
</table>
<br />
