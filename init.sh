#!/bin/bash

# Loads dbinit.sql into your running CockroachDB cluster
cockroach sql --insecure --url="postgres://root@127.0.0.1:26257" < dbinit.sql

envfile=".env"

# Resets .env file, clearing out any variables that were previously set
git checkout -- $envfile

# replace API_key with $MOVR_MAPS_API in `.env` for the following env variable:
#     API_KEY = 'API_key'
# where API_KEY is Google Geocoding API Key needed to generate maps on the Vehicles page.
sed -i -- "s/API_key/$MOVR_MAPS_API/" $envfile

echo ".env: API_KEY key has been set"
