"""Datapoint API to retrieve Met Office data"""

#__version__ = "0.7.0"
__author__ = "Jacob Tomlinson"
__author_email__ = "jacob.tomlinson@metoffice.gov.uk"

import os.path
from pkg_resources import get_distribution, DistributionNotFound

from datapoint.Manager import Manager
import datapoint.profile

# This block is from the setuptools_scm README
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # Package is not installed
    pass

def connection(profile_name='default', api_key=None):
    """Connect to DataPoint with the given API key profile name."""
    if api_key is None:
        profile_fname = datapoint.profile.API_profile_fname(profile_name)
        if not os.path.exists(profile_fname):
            raise ValueError('Profile not found in {}. Please install your API \n'
                             'key with datapoint.profile.install_API_key('
                             '"<YOUR-KEY>")'.format(profile_fname))
        with open(profile_fname) as fh:
            api_key = fh.readlines()
    return Manager(api_key=api_key)
