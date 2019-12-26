Getting started
===============

Getting started with DataPoint for Python is simple and you can write a
simple script which prints out data in just 6 lines of Python.

API Key
-------

To access DataPoint you need to
`register <http://www.metoffice.gov.uk/datapoint/API>`__ with the Met
Office and get yourself an API key. The process is simple and just
ensures that you don’t abuse the service.

Connecting to DataPoint
-----------------------

Now that we have an API key we can import the module:

::

   import datapoint

And create a connection to DataPoint:

::

   conn = datapoint.connection(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")

This creates a :ref:`manager` object which manages our connection and interacts
with DataPoint for us, we’ll discuss Manager Objects in depth later but for now
you just need to know that it looks after your API key and has a load of methods
to return data from DataPoint.

Getting data from DataPoint
---------------------------

So now that we have our Manager Object with a connection to DataPoint we can
request some data. Our goal is to request some forecast data but first we need
to know the site ID for the location we want data for. Luckily the Manager
Object has a method to return a :ref:`site` object, which contains the ID among
other things, from a specified latitude and longitude.

We can simply request a Site Object like so:

::

   site = conn.get_nearest_forecast_site(51.500728, -0.124626)

For now we’re just going to use this object to get us our forecast but
you’ll find more information about what the Site Object contains later.

Let’s call another of the Manager Object’s methods to give us a
:ref:`forecast` object for our site:

::

   forecast = conn.get_forecast_for_site(site.id, "3hourly")

We’ve given this method two parameters, the site ID for the forecast we want and
also a forecast type of “3hourly”. We’ll discuss the forecast types later on.

This Forecast Object which has been returned to us contains lots of information
which we will cover in a later section, right now we’re just going to get the
:ref:`timestep` object which represents right this minute:

::

   current_timestep = forecast.now()

This Timestep Object contains many different details about the weather
but for now we’ll just print out the weather text.

::

   print current_timestep.weather.text

And there you have it. If you followed all the steps you should have
printed out the current weather for your chosen location.

Further Examples
----------------

For more code examples please have a look in the `examples
folder <https://github.com/ejep/datapoint-python/tree/master/examples>`__
in the GitHub project.
