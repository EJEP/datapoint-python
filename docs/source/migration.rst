Migration from DataPoint
========================

The new APIs the Met Office provide via DataHub are very different in behaviour
to the old APIs which were provided via DataPoint. As such this library has
changed greatly.

The main changes are below.

No concept of 'sites'
---------------------

There is no concept of retrieving a site id for a location before requesting a
forecast. Now a latitude and longitude are provided to the library directly.

No observations
---------------

The new API does not provide 'observations' like DataPoint. However, the current
state of the weather is returned as part of the forecast responses. As such,
this library no longer provides separate 'observations'.

Simplified object hierarchy
---------------------------

Python dicts are used instead of classes to allow more flexibility with handling
data returned from the MetOffice API, and because new MetOffice API provides
data with a more convenient structure. The concept of 'Days' has also been
removed from the library and instead all time steps are provided in one list.
The data structure for a single time step is::

  {
       'time': datetime.datetime(2024, 2, 19, 13, 0, tzinfo=datetime.timezone.utc),
       'screenTemperature': {
           'value': 10.09,
           'description': 'Screen Air Temperature',
           'unit_name': 'degrees Celsius',
           'unit_symbol': 'Cel'
       },
       'screenDewPointTemperature': {
           'value': 8.08,
           'description': 'Screen Dew Point Temperature',
           'unit_name': 'degrees Celsius',
           'unit_symbol': 'Cel'
       },
       'feelsLikeTemperature': {
           'value': 6.85,
           'description': 'Feels Like Temperature',
           'unit_name': 'degrees Celsius',
           'unit_symbol': 'Cel'
       },
       'windSpeed10m': {
           'value': 7.57,
           'description': '10m Wind Speed',
           'unit_name': 'metres per second',
           'unit_symbol': 'm/s'
       },
       'windDirectionFrom10m': {
           'value': 263,
           'description': '10m Wind From Direction',
           'unit_name': 'degrees',
           'unit_symbol': 'deg'
       },
       'windGustSpeed10m': {
           'value': 12.31,
           'description': '10m Wind Gust Speed',
           'unit_name': 'metres per second',
           'unit_symbol': 'm/s'
       },
       'visibility': {
           'value': 21201,
           'description': 'Visibility',
           'unit_name': 'metres',
           'unit_symbol': 'm'
       },
       'screenRelativeHumidity': {
           'value': 87.81,
           'description': 'Screen Relative Humidity',
           'unit_name': 'percentage',
           'unit_symbol': '%'
       },
       'mslp': {
           'value': 103080,
           'description': 'Mean Sea Level Pressure',
           'unit_name': 'pascals',
           'unit_symbol': 'Pa'
       },
       'uvIndex': {
           'value': 1,
           'description': 'UV Index',
           'unit_name': 'dimensionless',
           'unit_symbol': '1'
       },
       'significantWeatherCode': {
           'value': 'Cloudy',
           'description': 'Significant Weather Code',
           'unit_name': 'dimensionless',
           'unit_symbol': '1'
       },
       'precipitationRate': {
           'value': 0.0,
           'description': 'Precipitation Rate',
           'unit_name': 'millimetres per hour',
           'unit_symbol': 'mm/h'
       },
       'probOfPrecipitation': {
           'value': 21,
           'description': 'Probability of Precipitation',
           'unit_name': 'percentage',
           'unit_symbol': '%'
       }
  }

Different data provided
-----------------------

There are some differences in what data are provided in each weather forecast
compared to the old DataPoint API, and in the names of the features.
