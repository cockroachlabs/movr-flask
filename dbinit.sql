SET sql_safe_updates = false;


DROP DATABASE IF EXISTS movr CASCADE; 


CREATE DATABASE movr PRIMARY REGION "gcp-us-east1" REGIONS "gcp-europe-west1", "gcp-us-west1";


USE movr;


CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    city STRING NOT NULL,
    first_name STRING NULL,
    last_name STRING NULL,
    email STRING NULL,
    username STRING NULL,
    password_hash STRING NULL,
    is_owner BOOL NULL,
    UNIQUE INDEX users_username_key (username ASC)
    ) LOCALITY REGIONAL BY ROW;


ALTER TABLE users ADD COLUMN region crdb_internal_region AS (
  CASE WHEN city = 'amsterdam' THEN 'gcp-europe-west1'
       WHEN city = 'paris' THEN 'gcp-europe-west1'
       WHEN city = 'rome' THEN 'gcp-europe-west1'
       WHEN city = 'new york' THEN 'gcp-us-east1'
       WHEN city = 'boston' THEN 'gcp-us-east1'
       WHEN city = 'washington dc' THEN 'gcp-us-east1'
       WHEN city = 'san francisco' THEN 'gcp-us-west1'
       WHEN city = 'seattle' THEN 'gcp-us-west1'
       WHEN city = 'los angeles' THEN 'gcp-us-west1'
       ELSE 'gcp-us-east1'
  END
) STORED;


CREATE TABLE IF NOT EXISTS vehicles (
    id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    city STRING NOT NULL,
    type STRING NULL,
    owner_id UUID NULL,
    date_added DATE NULL,
    status STRING NULL,
    last_location STRING NULL,
    color STRING NULL,
    brand STRING NULL,    
    CONSTRAINT fk_ref_users FOREIGN KEY (owner_id) REFERENCES users(id)
    ) LOCALITY REGIONAL BY ROW;


ALTER TABLE vehicles ADD COLUMN region crdb_internal_region AS (
  CASE WHEN city = 'amsterdam' THEN 'gcp-europe-west1'
       WHEN city = 'paris' THEN 'gcp-europe-west1'
       WHEN city = 'rome' THEN 'gcp-europe-west1'
       WHEN city = 'new york' THEN 'gcp-us-east1'
       WHEN city = 'boston' THEN 'gcp-us-east1'
       WHEN city = 'washington dc' THEN 'gcp-us-east1'
       WHEN city = 'san francisco' THEN 'gcp-us-west1'
       WHEN city = 'seattle' THEN 'gcp-us-west1'
       WHEN city = 'los angeles' THEN 'gcp-us-west1'
       ELSE 'gcp-us-east1'
  END
) STORED;


CREATE TABLE rides (
    id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    city STRING NOT NULL,
    vehicle_id UUID NULL,
    rider_id UUID NULL,
    start_location STRING NULL,
    end_location STRING NULL,
    start_time TIMESTAMPTZ NULL,
    end_time TIMESTAMPTZ NULL,
    length INTERVAL NULL,
    CONSTRAINT fk_city_ref_users FOREIGN KEY (rider_id) REFERENCES users(id),
    CONSTRAINT fk_vehicle_ref_vehicles FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
    );


ALTER TABLE rides ADD COLUMN region crdb_internal_region AS (
  CASE WHEN city = 'amsterdam' THEN 'gcp-europe-west1'
       WHEN city = 'paris' THEN 'gcp-europe-west1'
       WHEN city = 'rome' THEN 'gcp-europe-west1'
       WHEN city = 'new york' THEN 'gcp-us-east1'
       WHEN city = 'boston' THEN 'gcp-us-east1'
       WHEN city = 'washington dc' THEN 'gcp-us-east1'
       WHEN city = 'san francisco' THEN 'gcp-us-west1'
       WHEN city = 'seattle' THEN 'gcp-us-west1'
       WHEN city = 'los angeles' THEN 'gcp-us-west1'
       ELSE 'gcp-us-east1'
  END
) STORED;


INSERT INTO users (id, city, first_name, last_name, email, username) VALUES 
    ('2804df7c-d8fd-4b1c-9799-b1d44452554b', 'new york', 'Carl', 'Kimball', 'carl@cockroachlabs.com', 'carl');

INSERT INTO vehicles (id, city, type, owner_id, date_added, status, last_location, color, brand) VALUES 
    ('142b7c9e-6227-4dbb-b188-b1dac57d5521', 'new york', 'scooter', '2804df7c-d8fd-4b1c-9799-b1d44452554b', current_date(),'available', 'Time Square', 'Blue', 'Razor');

INSERT INTO rides(city, rider_id, vehicle_id, start_location, end_location, start_time, end_time, length) VALUES 
    ('new york', '2804df7c-d8fd-4b1c-9799-b1d44452554b', '142b7c9e-6227-4dbb-b188-b1dac57d5521', 'Cockroach Labs, 23rd Street', 'Time Square', '2020-01-16 21:20:48.224453+00:00', '2020-01-16 21:20:52.045813+00:00', '00:00:03.82136');
