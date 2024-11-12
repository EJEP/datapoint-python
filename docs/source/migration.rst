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
data with a more convenient structure.

Different data provided
-----------------------

There are some differences in what data are provided in each weather forecast
compared to the old DataPoint API, and in the names of the features.
