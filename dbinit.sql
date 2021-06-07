SET sql_safe_updates = FALSE;

DROP DATABASE IF EXISTS movr CASCADE;

CREATE DATABASE movr PRIMARY REGION "gcp-us-east1" REGIONS "gcp-us-east1", "gcp-europe-west1", "gcp-us-west1";

USE movr;

CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
  city STRING NOT NULL,
  first_name STRING,
  last_name STRING,
  email STRING,
  username STRING,
  password_hash STRING,
  is_owner bool,
  UNIQUE INDEX users_username_key (username ASC)) 
  LOCALITY REGIONAL BY ROW;

CREATE TABLE vehicles (
    id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    type STRING,
    city STRING,
    owner_id UUID,
    date_added date,
    status STRING,
    last_location STRING,
    color STRING,
    brand STRING, 
    CONSTRAINT fk_ref_users FOREIGN KEY (owner_id) REFERENCES users (id))
    LOCALITY REGIONAL BY ROW;

CREATE TABLE rides (
  id uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
  city STRING NOT NULL,
  vehicle_id uuid,
  rider_id uuid,
  start_location STRING,
  end_location STRING,
  start_time timestamptz,
  end_time timestamptz,
  length interval,
  CONSTRAINT fk_city_ref_users FOREIGN KEY (rider_id) REFERENCES users (id),
  CONSTRAINT fk_vehicle_ref_vehicles FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)) 
  LOCALITY REGIONAL BY ROW;

INSERT INTO users (id, city, first_name, last_name, email, username)
  VALUES ('2804df7c-d8fd-4b1c-9799-b1d44452554b', 'new york', 'Carl', 'Kimball', 'carl@cockroachlabs.com', 'carl');

INSERT INTO vehicles (id, city, type, owner_id, date_added, status, last_location, color, brand)
  VALUES ('142b7c9e-6227-4dbb-b188-b1dac57d5521', 'new york', 'scooter', '2804df7c-d8fd-4b1c-9799-b1d44452554b', current_date(), 'available', 'Time Square', 'Blue', 'Razor');

INSERT INTO rides (city, rider_id, vehicle_id, start_location, end_location, start_time, end_time, length)
  VALUES ('new york', '2804df7c-d8fd-4b1c-9799-b1d44452554b', '142b7c9e-6227-4dbb-b188-b1dac57d5521', 'Cockroach Labs, 23rd Street', 'Time Square', '2020-01-16 21:20:48.224453+00:00', '2020-01-16 21:20:52.045813+00:00', '00:00:03.82136');

