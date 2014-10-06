import os

import appdirs


def API_profile_fname(profile_name='default'):
    """Get the API key profile filename."""
    return os.path.join(appdirs.user_data_dir('DataPoint'),
                        profile_name + '.key')


def install_API_key(api_key, profile_name='default'):
    """Put the given API key into the given profile name."""
    fname = API_profile_fname(profile_name)
    if not os.path.isdir(os.path.dirname(fname)):
        os.makedirs(os.path.dirname(fname))
    with open(fname, 'w') as fh:
        fh.write(api_key)
