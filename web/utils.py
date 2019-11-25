# This file contains utility functions

def get_region(city):
    if city in ('new york', 'boston', 'washington_dc'):
        return 'gcp-us-east1'
    elif city in ('san francisco', 'seattle', 'los angeles'):
        return 'gcp-us-west1'
    elif city in ('amsterdam', 'paris', 'rome'):
        return 'gcp-europe-west1'
    else:
        return None
