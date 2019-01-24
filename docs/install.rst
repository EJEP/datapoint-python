DataPoint for Python can be installed like any other Python module.

It is available on `PyPI <https://pypi.python.org/pypi/datapoint/>`__
and the source is available on
`GitHub <https://github.com/jacobtomlinson/datapoint-python>`__.

Pip
---

`Pip <https://pip.pypa.io/>`__ makes Python package installation simple.
For the latest stable version just fire up your terminal and run:

::

   pip install datapoint

or for the very latest code from the repository’s master branch run:

::

   pip install git+git://github.com/jacobtomlinson/datapoint-python.git@master

and to upgrade it in the future:

::

   pip install git+git://github.com/jacobtomlinson/datapoint-python.git@master --upgrade

Easy Install
------------

Or if you really feel the need then you can use
`easy_install <http://pypi.python.org/pypi/setuptools>`__.

::

   easy_install datapoint

But you `probably
shouldn’t <https://stackoverflow.com/questions/3220404/why-use-pip-over-easy-install>`__.

Source
------

You can also install from the source in GitHub.

First checkout the GitHub repository (or you can `download the
zip <https://github.com/jacobtomlinson/datapoint-python/archive/master.zip>`__
and extract it).

::

   git clone https://github.com/jacobtomlinson/datapoint-python.git datapoint-python

Navigate to that directory

::

   cd datapoint-python

Then run the setup

::

   python setup.py install

Windows
-------

-  Install `python <https://www.python.org/downloads/>`__ - you can see
   supported versions in the
   `readme <https://github.com/jacobtomlinson/datapoint-python/blob/master/README.md>`__
-  Install the appropriate
   `setuptools <http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools>`__
   python extension for your machine
-  Install the appropriate
   `pip <http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip>`__ python
   extension for your machine
-  Add pip to your environment variables:

   -  Run **Start** > **Edit the environment variables for your
      account**
   -  Create a new variable:
   -  **name** pip
   -  **value** the path to **pip.exe** (this should be something like
      C::raw-latex:`\Python`27:raw-latex:`\Scripts`)

-  From the command line run **pip install datapoint**
