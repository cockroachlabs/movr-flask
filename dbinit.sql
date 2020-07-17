SET sql_safe_updates = false;


DROP DATABASE IF EXISTS movr CASCADE; 


CREATE DATABASE movr;


USE movr;


CREATE TABLE IF NOT EXISTS users (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    region STRING NOT NULL,
    city STRING NOT NULL,
    first_name STRING NULL,
    last_name STRING NULL,
    email STRING NULL,
    username STRING NULL,
    password_hash STRING NULL,
    is_owner BOOL NULL,
    CONSTRAINT "primary" PRIMARY KEY (region ASC, id ASC),
    UNIQUE INDEX users_username_key (username ASC),
    FAMILY "primary" (id, region, city, first_name, last_name, email, username, password_hash, is_owner)
) PARTITION BY LIST (region) (
    PARTITION us_west VALUES IN (('gcp-us-west1')),
    PARTITION us_east VALUES IN (('gcp-us-east1')),
    PARTITION europe_west VALUES IN (('gcp-europe-west1'))
);

ALTER PARTITION europe_west OF INDEX movr.public.users@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-europe-west1]';
ALTER PARTITION us_east OF INDEX movr.public.users@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-east1]';
ALTER PARTITION us_west OF INDEX movr.public.users@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-west1]'
;


CREATE TABLE IF NOT EXISTS vehicles (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    region STRING NOT NULL,
    city STRING NOT NULL,
    type STRING NULL,
    owner_id UUID NULL,
    date_added DATE NULL,
    status STRING NULL,
    last_location STRING NULL,
    color STRING NULL,
    brand STRING NULL,
    CONSTRAINT "primary" PRIMARY KEY (region ASC, id ASC),
    INDEX vehicles_available_idx (region ASC, city ASC, owner_id ASC, status ASC) PARTITION BY LIST (region) (
        PARTITION us_west VALUES IN (('gcp-us-west1')),
        PARTITION us_east VALUES IN (('gcp-us-east1')),
        PARTITION europe_west VALUES IN (('gcp-europe-west1'))
    ),
    CONSTRAINT fk_region_ref_users FOREIGN KEY (region, owner_id) REFERENCES users(region, id),
    INDEX vehicles_index_fk_region_ref_users (region ASC, owner_id ASC) PARTITION BY LIST (region) (
        PARTITION us_west VALUES IN (('gcp-us-west1')),
        PARTITION us_east VALUES IN (('gcp-us-east1')),
        PARTITION europe_west VALUES IN (('gcp-europe-west1'))
    ),
    FAMILY "primary" (id, region, city, type, owner_id, date_added, status, last_location, color, brand)
) PARTITION BY LIST (region) (
    PARTITION us_west VALUES IN (('gcp-us-west1')),
    PARTITION us_east VALUES IN (('gcp-us-east1')),
    PARTITION europe_west VALUES IN (('gcp-europe-west1'))
);

ALTER PARTITION europe_west OF INDEX movr.public.vehicles@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-europe-west1]';
ALTER PARTITION us_east OF INDEX movr.public.vehicles@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-east1]';
ALTER PARTITION us_west OF INDEX movr.public.vehicles@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-west1]';
ALTER PARTITION europe_west OF INDEX movr.public.vehicles@vehicles_index_fk_region_ref_users CONFIGURE ZONE USING
    constraints = '[+region=gcp-europe-west1]';
ALTER PARTITION us_east OF INDEX movr.public.vehicles@vehicles_index_fk_region_ref_users CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-east1]';
ALTER PARTITION us_west OF INDEX movr.public.vehicles@vehicles_index_fk_region_ref_users CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-west1]'
;


CREATE TABLE rides (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    region STRING NOT NULL,
    city STRING NOT NULL,
    vehicle_id UUID NULL,
    rider_id UUID NULL,
    rider_region STRING NOT NULL,
    start_location STRING NULL,
    end_location STRING NULL,
    start_time TIMESTAMPTZ NULL,
    end_time TIMESTAMPTZ NULL,
    length INTERVAL NULL,
    CONSTRAINT "primary" PRIMARY KEY (region ASC, id ASC),
    CONSTRAINT fk_region_ref_users FOREIGN KEY (rider_region, rider_id) REFERENCES users(region, id),
    CONSTRAINT fk_vehicle_region_ref_vehicles FOREIGN KEY (region, vehicle_id) REFERENCES vehicles(region, id),
    INDEX rides_index_fk_region_ref_users (rider_region ASC, rider_id ASC) PARTITION BY LIST (rider_region) (
        PARTITION us_west VALUES IN (('gcp-us-west1')),
        PARTITION us_east VALUES IN (('gcp-us-east1')),
        PARTITION europe_west VALUES IN (('gcp-europe-west1'))
    ),
    INDEX rides_index_fk_vehicle_region_ref_vehicles (region ASC, vehicle_id ASC) PARTITION BY LIST (region) (
        PARTITION us_west VALUES IN (('gcp-us-west1')),
        PARTITION us_east VALUES IN (('gcp-us-east1')),
        PARTITION europe_west VALUES IN (('gcp-europe-west1'))
    ),
    FAMILY "primary" (id, region, rider_id, rider_region, vehicle_id, start_location, end_location, start_time, end_time, length)
)  PARTITION BY LIST (region) (
    PARTITION us_west VALUES IN (('gcp-us-west1')),
    PARTITION us_east VALUES IN (('gcp-us-east1')),
    PARTITION europe_west VALUES IN (('gcp-europe-west1'))
);

ALTER PARTITION europe_west OF INDEX movr.public.rides@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-europe-west1]';
ALTER PARTITION us_east OF INDEX movr.public.rides@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-east1]';
ALTER PARTITION us_west OF INDEX movr.public.rides@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-west1]';
ALTER PARTITION europe_west OF INDEX movr.public.rides@rides_index_fk_region_ref_users CONFIGURE ZONE USING
    constraints = '[+region=gcp-europe-west1]';
ALTER PARTITION us_east OF INDEX movr.public.rides@rides_index_fk_region_ref_users CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-east1]';
ALTER PARTITION us_west OF INDEX movr.public.rides@rides_index_fk_region_ref_users CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-west1]';
ALTER PARTITION europe_west OF INDEX movr.public.rides@rides_index_fk_vehicle_region_ref_vehicles CONFIGURE ZONE USING
    constraints = '[+region=gcp-europe-west1]';
ALTER PARTITION us_east OF INDEX movr.public.rides@rides_index_fk_vehicle_region_ref_vehicles CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-east1]';
ALTER PARTITION us_west OF INDEX movr.public.rides@rides_index_fk_vehicle_region_ref_vehicles CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-west1]'
;


INSERT INTO users (id, region, city, first_name, last_name, email, username) VALUES 
    ('2804df7c-d8fd-4b1c-9799-b1d44452554b', 'gcp-us-east1', 'new york', 'Carl', 'Kimball', 'carl@cockroachlabs.com', 'carl');

INSERT INTO vehicles (id, region, city, type, owner_id, date_added, status, last_location, color, brand) VALUES 
    ('142b7c9e-6227-4dbb-b188-b1dac57d5521', 'gcp-us-east1', 'new york', 'scooter', '2804df7c-d8fd-4b1c-9799-b1d44452554b', current_date(),'available', 'Time Square', 'Blue', 'Razor');

INSERT INTO rides(city, region, rider_id, rider_region, vehicle_id, start_location, end_location, start_time, end_time, length) VALUES 
    ('new york', 'gcp-us-east1', '2804df7c-d8fd-4b1c-9799-b1d44452554b', 'gcp-us-east1', '142b7c9e-6227-4dbb-b188-b1dac57d5521', 'Cockroach Labs, 23rd Street', 'Time Square', '2020-01-16 21:20:48.224453+00:00', '2020-01-16 21:20:52.045813+00:00', '00:00:03.82136');
