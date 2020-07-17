# This file contains utility functions
from geopy.geocoders import Nominatim

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
        try:
            geolocator = Nominatim(user_agent='MovR-Flask')
            long = geolocator.geocode(city).longitude
            # Place in US East region if between Dallas,TX and Nuuk,Greenland
            if (long >= -96 and long <= -52):
                return 'gcp-us-east1'
            # Place in US West region if between Dallas,TX and Hong Kong
            if (long <= -96 or long >= 118):
                return 'gcp-us-west1'
            # Place all else in Europe West region
            else:
                return 'gcp-europe-west1'
        except Exception:
            raise
