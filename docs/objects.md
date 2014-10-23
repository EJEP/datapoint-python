# Objects

DataPoint for Python makes use of objects for almost everything.
There are 6 different objects which will be returned by the module.

## Manager
The object which stores your API key and has methods to access the API.

### Properties

#### api_key

_(string)_ The DataPoint API key used when initialising the object.

### Methods

#### get_all_sites()

Arguments:
None
Returns:
_(list)_ A list of all Site objects.

## Site
An object containing details about a specific forecast site.

## Forecast
An object with properties of a single forecast and a list of Day objects.

## Day
An object with properties of a single day and a list of Timestep objects.

## Timestep
An object with each forecast property (wind, temp, etc) for a specific time,
in the form of Element objects.

## Element
An object with properties about a specific weather element.
