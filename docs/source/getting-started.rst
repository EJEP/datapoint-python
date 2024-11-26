Getting started
===============

Getting started with DataHub for Python is simple and you can write a
simple script which prints out data in just 6 lines of Python.

API Key
-------

To access DataPoint you need to `register <https://datahub.metoffice.gov.uk/>`__
with the Met Office and get yourself an API key. The process is simple and just
ensures that you don’t abuse the service. You will need access to the
Site-Specific forecast API.

Connecting to DataHub
-----------------------

Now that you have an API key you can import the module:

::

   import datapoint

And create a connection to DataHub:

::

   manager = datapoint.Manager(api_key="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")

This creates a `manager` object which manages the connection and interacts
with DataHub.

Getting data from DataHub
---------------------------

So now that you have a Manager object with a connection to DataHub you can
request some data. To do this, use the `manager` object:

::

   forecast = manager.get_forecast(51, 0, "hourly", convert_weather_code=True)

This takes four parameters: the latitude and longitude of the location you want
a forecast for, a forecast type of “hourly” and an instruction to convert the
numeric weather code to a string description. We’ll discuss the forecast types
later on.

This Forecast Object which has been returned to us contains lots of information
which we will cover in a later section, right now we’re just going to get the
data for the current time:

::

   current_weather = forecast.now()

This is a dict which contains many different details about the weather
but for now we’ll just print out one field.

::

   print(current_weather["feelsLikeTemperature"])

And there you have it. If you followed all the steps you should have
printed out the current weather for your chosen location.

Further Examples
----------------

For more code examples please have a look in the `examples
folder <https://github.com/ejep/datapoint-python/tree/master/examples>`__
in the GitHub project.
