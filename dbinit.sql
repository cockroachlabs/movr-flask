SET sql_safe_updates = false;


DROP DATABASE IF EXISTS movr CASCADE; 


CREATE DATABASE movr;


USE movr;


CREATE TABLE IF NOT EXISTS users (
    id UUID NOT NULL,
    city STRING NOT NULL,
    first_name STRING NULL,
    last_name STRING NULL,
    email STRING NULL,
    username STRING NULL,
    password_hash STRING NULL,
    is_owner BOOL NULL,
    CONSTRAINT "primary" PRIMARY KEY (city ASC, id ASC),
    CONSTRAINT check_city CHECK (city IN ('amsterdam','boston','los angeles','new york','paris','rome','san francisco','seattle','washington dc')),
    UNIQUE INDEX users_username_key (username ASC),
    FAMILY "primary" (id, city, first_name, last_name, email, username, password_hash, is_owner)
) PARTITION BY LIST (city) (
    PARTITION us_west VALUES IN (('seattle'), ('san francisco'), ('los angeles')),
    PARTITION us_east VALUES IN (('new york'), ('boston'), ('washington dc')),
    PARTITION europe_west VALUES IN (('amsterdam'), ('paris'), ('rome'))
);

ALTER PARTITION europe_west OF INDEX movr.public.users@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-europe-west1]';
ALTER PARTITION us_east OF INDEX movr.public.users@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-east1]';
ALTER PARTITION us_west OF INDEX movr.public.users@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-west1]'
;


CREATE TABLE IF NOT EXISTS vehicles (
    id UUID NOT NULL,
    city STRING NOT NULL,
    type STRING NULL,
    owner_id UUID NULL,
    date_added DATE NULL,
    status STRING NULL,
    last_location STRING NULL,
    color STRING NULL,
    brand STRING NULL,
    CONSTRAINT "primary" PRIMARY KEY (city ASC, id ASC),
    CONSTRAINT check_city CHECK (city IN ('amsterdam','boston','los angeles','new york','paris','rome','san francisco','seattle','washington dc')),      
    CONSTRAINT fk_city_ref_users FOREIGN KEY (city, owner_id) REFERENCES users(city, id),
    INDEX vehicles_auto_index_fk_city_ref_users (city ASC, owner_id ASC, status ASC) PARTITION BY LIST (city) (
        PARTITION us_west VALUES IN (('seattle'), ('san francisco'), ('los angeles')),
        PARTITION us_east VALUES IN (('new york'), ('boston'), ('washington dc')),
        PARTITION europe_west VALUES IN (('amsterdam'), ('paris'), ('rome'))
    ),
    FAMILY "primary" (id, city, type, owner_id, date_added, status, last_location, color, brand)
) PARTITION BY LIST (city) (
    PARTITION us_west VALUES IN (('seattle'), ('san francisco'), ('los angeles')),
    PARTITION us_east VALUES IN (('new york'), ('boston'), ('washington dc')),
    PARTITION europe_west VALUES IN (('amsterdam'), ('paris'), ('rome'))
);

ALTER PARTITION europe_west OF INDEX movr.public.vehicles@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-europe-west1]';
ALTER PARTITION us_east OF INDEX movr.public.vehicles@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-east1]';
ALTER PARTITION us_west OF INDEX movr.public.vehicles@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-west1]';
ALTER PARTITION europe_west OF INDEX movr.public.vehicles@vehicles_auto_index_fk_city_ref_users CONFIGURE ZONE USING
    constraints = '[+region=gcp-europe-west1]';
ALTER PARTITION us_east OF INDEX movr.public.vehicles@vehicles_auto_index_fk_city_ref_users CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-east1]';
ALTER PARTITION us_west OF INDEX movr.public.vehicles@vehicles_auto_index_fk_city_ref_users CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-west1]'
;


CREATE TABLE rides (
    id UUID NOT NULL,
    city STRING NOT NULL,
    vehicle_id UUID NULL,
    rider_id UUID NULL,
    rider_city STRING NOT NULL,
    start_location STRING NULL,
    end_location STRING NULL,
    start_time TIMESTAMP NULL,
    end_time TIMESTAMP NULL,
    length INTERVAL NULL,
    CONSTRAINT "primary" PRIMARY KEY (city ASC, id ASC),
    CONSTRAINT check_city CHECK (city IN ('amsterdam','boston','los angeles','new york','paris','rome','san francisco','seattle','washington dc')),
    CONSTRAINT fk_city_ref_users FOREIGN KEY (rider_city, rider_id) REFERENCES users(city, id),
    CONSTRAINT fk_vehicle_city_ref_vehicles FOREIGN KEY (city, vehicle_id) REFERENCES vehicles(city, id),
    INDEX rides_auto_index_fk_city_ref_users (rider_city ASC, rider_id ASC) PARTITION BY LIST (rider_city) (
        PARTITION us_west VALUES IN (('seattle'), ('san francisco'), ('los angeles')),
        PARTITION us_east VALUES IN (('new york'), ('boston'), ('washington dc')),
        PARTITION europe_west VALUES IN (('amsterdam'), ('paris'), ('rome'))
    ),
    INDEX rides_auto_index_fk_vehicle_city_ref_vehicles (city ASC, vehicle_id ASC) PARTITION BY LIST (city) (
        PARTITION us_west VALUES IN (('seattle'), ('san francisco'), ('los angeles')),
        PARTITION us_east VALUES IN (('new york'), ('boston'), ('washington dc')),
        PARTITION europe_west VALUES IN (('amsterdam'), ('paris'), ('rome'))
    ),
    FAMILY "primary" (id, city, rider_id, rider_city, vehicle_id, start_location, end_location, start_time, end_time, length)
)  PARTITION BY LIST (city) (
        PARTITION us_west VALUES IN (('seattle'), ('san francisco'), ('los angeles')),
        PARTITION us_east VALUES IN (('new york'), ('boston'), ('washington dc')),
        PARTITION europe_west VALUES IN (('amsterdam'), ('paris'), ('rome'))
);
ALTER PARTITION europe_west OF INDEX movr.public.rides@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-europe-west1]';
ALTER PARTITION us_east OF INDEX movr.public.rides@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-east1]';
ALTER PARTITION us_west OF INDEX movr.public.rides@primary CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-west1]';
ALTER PARTITION europe_west OF INDEX movr.public.rides@rides_auto_index_fk_city_ref_users CONFIGURE ZONE USING
    constraints = '[+region=gcp-europe-west1]';
ALTER PARTITION us_east OF INDEX movr.public.rides@rides_auto_index_fk_city_ref_users CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-east1]';
ALTER PARTITION us_west OF INDEX movr.public.rides@rides_auto_index_fk_city_ref_users CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-west1]';
ALTER PARTITION europe_west OF INDEX movr.public.rides@rides_auto_index_fk_vehicle_city_ref_vehicles CONFIGURE ZONE USING
    constraints = '[+region=gcp-europe-west1]';
ALTER PARTITION us_east OF INDEX movr.public.rides@rides_auto_index_fk_vehicle_city_ref_vehicles CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-east1]';
ALTER PARTITION us_west OF INDEX movr.public.rides@rides_auto_index_fk_vehicle_city_ref_vehicles CONFIGURE ZONE USING
    constraints = '[+region=gcp-us-west1]'
;

