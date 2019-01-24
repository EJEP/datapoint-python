Objects
=======

DataPoint for Python makes use of objects for almost everything. There
are 6 different objects which will be returned by the module.

The diagram below shows the main classes used by the library, and how to
move between them.

.. figure:: https://cloud.githubusercontent.com/assets/9357195/4751636/83f178cc-5aa0-11e4-8eb0-a1b9531ed319.png
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

get_all_sites()
'''''''''''''''

Returns a list of all available sites. returns: list of Site objects

get_nearest_site(latitude=False, longitude=False)
'''''''''''''''''''''''''''''''''''''''''''''''''

Returns the nearest Site object to the specified coordinates. param
latitude: int or float param longitude: int or float returns: Site

get_forecast_for_site(site_id, frequency=“daily”):
''''''''''''''''''''''''''''''''''''''''''''''''''

Get a forecast for the provided site. A frequency of “daily” will return
two timesteps: “Day” and “Night”. A frequency of “3hourly” will return 8
timesteps: 0, 180, 360 … 1260 (minutes since midnight UTC) param
site_id: string or unicode param frequency: string (“daily” or
“3hourly”) returns: Forecast

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

Get the current timestep from this forecast returns: Timestep (or False)

Day
---

An object with properties of a single day and a list of Timestep
objects.

.. _attributes-3:

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

.. _attributes-4:

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

.. _attributes-5:

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
