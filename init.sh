#!/bin/bash

# Loads dbinit.sql into your running CockroachDB cluster
cockroach sql --insecure --url="postgres://root@127.0.0.1:$MOVR_PORT" < dbinit.sql

# Resets .env file, clearing out any variables that were previously set
git checkout -- .env

# replace <port> with $MOVR_PORT in `.env` for the following env variable:
#     DB_URI = 'cockroachdb://root@127.0.0.1:<port>/movr'
# where DB_URI is the SQL connection string needed for SQLAlchemy to connect to CockroachDB.
sed "s/<port>/$MOVR_PORT/" .env  > temp

# replace API_key with $MOVR_MAPS_API in `.env` for the following env variable:
#     API_KEY = 'API_key'
# where API_KEY is Google Maps Static API Key needed to generate maps on the Vehicles page.
sed "s/API_key/$MOVR_MAPS_API/" temp  > .env

# clean up temp file
rm temp > /dev/null

echo ".env: DB_URI and API_KEY keys have been set"
