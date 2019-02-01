Objects
=======

DataPoint for Python makes use of objects for almost everything. There
are 6 different objects which will be returned by the module.

The diagram below shows the main classes used by the library, and how to
move between them.

.. figure:: https://user-images.githubusercontent.com/22224469/51768591-a54fb580-20d8-11e9-851a-cbc3dc434cca.png
   :alt: classes

   classes

Manager
-------

The object which stores your API key and has methods to access the API.

Attributes
^^^^^^^^^^

==================  ====================
attribute           type
------------------  --------------------
api_key             string
call_response       dict
sites_last_update   float
sites_last_request  list of Site objects
sites_update_time   int
==================  ====================

Methods
^^^^^^^

get_forecast_sites()
'''''''''''''''

Returns a list of available forecast sites.

- returns: list of Site objects

get_nearest_forecast_site(latitude=False, longitude=False)
'''''''''''''''''''''''''''''''''''''''''''''''''

Returns the nearest Site object to the specified coordinates which can provide a forecast.

- param latitude: int or float
- param longitude: int or float

- returns: Site

get_forecast_for_site(site_id, frequency=“daily”):
''''''''''''''''''''''''''''''''''''''''''''''''''

Get a forecast for the provided site. A frequency of “daily” will return
two timesteps: “Day” and “Night”. A frequency of “3hourly” will return 8
timesteps: 0, 180, 360 … 1260 (minutes since midnight UTC)

- param site_id: string or unicode
- param frequency: string (“daily” or “3hourly”)

- returns: Forecast

get_observation_sites()
'''''''''''''''''''''''

Returns a list of sites for which observations are available.

- returns: list of Site objects

get_nearest_observation_site(longitude=False, latitude=False)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Returns the nearest Site object to the specified coordinates.

- param longitude: int or float
- param latitude: int or float

- returns: Site

get_observations_for_site(site_id, frequency='hourly')
''''''''''''''''''''''''''''''''''''''''''''''''''''''

Get the observations for the provided site.
Only hourly observations are available, and provide the last 24 hours of data.

- param site_id: string or unicode
- param frequency: string ("daily" or "3hourly")

- returns: Observation


Site
----

An object containing details about a specific forecast site.

.. _attributes-1:

Attributes
^^^^^^^^^^

===============  =======
attribute        type
---------------  -------
api_key          string
name             unicode
id               unicode
elevation        unicode
latitude         unicode
longitude        unicode
nationalPark     unicode
region           unicode
unitaryAuthArea  unicode
===============  =======


Forecast
--------

An object with properties of a single forecast and a list of Day
objects.

.. _attributes-2:

Attributes
^^^^^^^^^^

==========  ===================
attribute   type
----------  -------------------
api_key     string
data_date   datetime
continent   unicode
country     unicode
name        unicode
longitude   unicode
latitude    unicode
id          unicode
elevation   unicode
days        list of Day objects
==========  ===================

.. _methods-1:

Methods
^^^^^^^

now()
'''''

Get the current timestep from this forecast

- returns: Timestep (or False)

Observation
-----------

An object with the properties of a single observation and a list of Day objects.

.. _attributes-3:

Attributes
^^^^^^^^^^

==========  ===================
attribute   type
----------  -------------------
api_key     string
data_date   datetime
continent   unicode
country     unicode
name        unicode
longitude   unicode
latitude    unicode
id          unicode
elevation   unicode
days        list of Day objects
==========  ===================


.. _methods-2:

Methods
^^^^^^^

now()
'''''

Get the current timestep from this observation

- returns: Timestep



Day
---

An object with properties of a single day and a list of Timestep
objects.

.. _attributes-4:

Attributes
^^^^^^^^^^

=========  ========================
attribute  type
---------  ------------------------
api_key    string
date       datetime
timesteps  list of Timestep objects
=========  ========================


Timestep
--------

An object with each forecast property (wind, temp, etc) for a specific
time, in the form of Element objects.

.. _attributes-5:

Attributes
^^^^^^^^^^

======================  ========================
attribute               type
----------------------  ------------------------
api_key                 string
name                    string
date                    datetime
weather                 Element
temperature             Element
feels_like_temperature  Element
wind_speed              Element
wind_direction          Element
wind_gust               Element
visibility              Element
uv                      Element
precipitation           Element
humidity                Element
======================  ========================


Element
-------

An object with properties about a specific weather element.

.. _attributes-6:

Attributes
^^^^^^^^^^

=========  ====================
attribute  type
---------  --------------------
id         string
value      int, float or string
units      unicode
text       string or None
=========  ====================
