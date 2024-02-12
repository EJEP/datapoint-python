"""Datapoint API to retrieve Met Office data"""

import os.path

from datapoint.Manager import Manager
import datapoint.profile


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

from . import _version
__version__ = _version.get_versions()['version']
