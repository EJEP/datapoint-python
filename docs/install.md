DataPoint for Python can be installed like any other Python module.

It is available on [PyPI][1] and the source is available on [GitHub][2].

## Pip

[Pip][3] makes Python package installation simple. Just fire up your terminal and run:

```
pip install datapoint
```

## Easy Install

Or if you really feel the need then you can use [easy_install][4].

```
easy_install datapoint
```

But you [probably shouldn't][5].

## Source

You can also install from the source in GitHub.

First checkout the GitHub repository (or you can [download the zip][6] and extract it).

```
git clone https://github.com/jacobtomlinson/datapoint-python.git datapoint-python
```

Navigate to that directory

```
cd datapoint-python
```

Then run the setup

```
python setup.py install
```

## Windows

* Install [python](https://www.python.org/downloads/) - you can see supported versions in the [readme](https://github.com/jacobtomlinson/datapoint-python/blob/master/README.md)
* Install the appropriate [setuptools](http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools) python extension for your machine
* Install the appropriate [pip](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip) python extension for your machine
* Add pip to your environment variables:
  *  Run **Start** > **Edit the environment variables for your account**
  *  Create a new variable:
    *    **name** pip
    *    **value** the path to **pip.exe** (this should be something like C:\Python27\Scripts)
* From the command line run **pip install datapoint**

[1]: https://pypi.python.org/pypi/datapoint/
[2]: https://github.com/jacobtomlinson/datapoint-python
[3]: https://pip.pypa.io/
[4]: http://pypi.python.org/pypi/setuptools
[5]: https://stackoverflow.com/questions/3220404/why-use-pip-over-easy-install
[6]: https://github.com/jacobtomlinson/datapoint-python/archive/master.zip
