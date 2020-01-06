# This file contains utility functions


def get_region(city):
    """Returns the cloud provider region closest to a supported city. Note that the region names are specific to the cloud provider, and must match the database locality region names.

    Arguments:
        city {String} -- The client's city. In production, the city is included in the header. In development, the city takes the default value `new york`.

    Returns:
        String -- The cloud provider region closest to the client's location.
    """
    if city in ('new york', 'boston', 'washington_dc'):
        return 'gcp-us-east1'
    elif city in ('san francisco', 'seattle', 'los angeles'):
        return 'gcp-us-west1'
    elif city in ('amsterdam', 'paris', 'rome'):
        return 'gcp-europe-west1'
    else:
        return None
