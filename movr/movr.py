from movr.transactions import start_ride_txn, end_ride_txn, add_user_txn, add_vehicle_txn, get_users_txn, get_user_txn, get_vehicles_txn, get_rides_txn, remove_user_txn, remove_vehicle_txn
from cockroachdb.sqlalchemy import run_transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import registry
registry.register("cockroachdb", "cockroachdb.sqlalchemy.dialect",
                  "CockroachDBDialect")


class MovR:
    """
    Wraps the database connection. The class methods wrap database transactions.
    """
    def __init__(self, conn_string):
        """
        Establish a connection to the database, creating an Engine instance.

        Arguments:
            conn_string {String} -- CockroachDB connection string.
        """
        self.engine = create_engine(conn_string, convert_unicode=True)

    def start_ride(self, region, city, rider_id, rider_city, vehicle_id):
        """
        Wraps a `run_transaction` call that starts a ride.

        Arguments:
            region {String} -- The ride's region.
            city {String} -- The ride's city.
            rider_id {UUID} -- The user's unique ID.
            rider_city {String} -- The user's city.
            vehicle_id {UUID} -- The vehicle's unique ID.
        """
        return run_transaction(
            sessionmaker(bind=self.engine), lambda session: start_ride_txn(
                session, region, city, rider_id, rider_city, vehicle_id))

    def end_ride(self, region, ride_id, location):
        """
        Wraps a `run_transaction` call that ends a ride.

        Arguments:
            region {String} -- The ride's region.
            ride_id {UUID} -- The ride's unique ID.
            location {String} -- The vehicle's last location.
        """
        return run_transaction(
            sessionmaker(bind=self.engine),
            lambda session: end_ride_txn(session, region, ride_id, location))

    def add_user(self, region, city, first_name, last_name, email, username, password):
        """
        Wraps a `run_transaction` call that adds a user.

        Arguments:
            region {String} -- The user's region.
            city {String} -- The user's city.
            first_name {String} -- The user's first name.
            last_name {String} -- The user's last name.
            email {String} -- The user's email.
            username {String} -- The user's username.
            password {String} -- The user's unhashed password.
        """
        return run_transaction(
            sessionmaker(bind=self.engine),
            lambda session: add_user_txn(session, region, city, first_name, last_name,
                                         email, username, password))

    def remove_user(self, region, user_id):
        """
        Wraps a `run_transaction` call that "removes" a user. No rows are deleted by this function.

        Arguments:
            region {String} -- The user's region.
            id {UUID} -- The user's unique ID.
        """
        return run_transaction(
            sessionmaker(bind=self.engine),
            lambda session: remove_user_txn(session, region, user_id))

    def remove_vehicle(self, region, vehicle_id):
        """
        Wraps a `run_transaction` call that "removes" a vehicle. No rows are deleted by this function.

        Arguments:
            region {String} -- The vehicle's region.
            id {UUID} -- The vehicle's unique ID.
        """
        return run_transaction(
            sessionmaker(bind=self.engine),
            lambda session: remove_vehicle_txn(session, region, vehicle_id))

    def add_vehicle(self,
                    region,
                    city,
                    owner_id,
                    last_location,
                    type,
                    color,
                    brand,
                    status,
                    is_owner=False):
        """
        Wraps a `run_transaction` call that adds a vehicle.

        Arguments:
            region {String} -- The vehicle's region.
            city {String} -- The vehicle's city.
            owner_id {UUID} -- The owner's unique ID.
            last_location {String} -- The vehicle's location.
            type {String} -- The vehicle's type.
            color {String} -- The vehicle's color.
            brand {String} -- The vehicle's brand.
            status {String} -- The vehicle's availability.

        Keyword Arguments:
            is_owner {bool} -- The owner status of the user, before the vehicle is added. (default: {False})
        """
        return run_transaction(
            sessionmaker(bind=self.engine), lambda session: add_vehicle_txn(
                session, region, city, owner_id, last_location, type, color, brand,
                status, is_owner))

    def get_users(self, region, city):
        """
        Wraps a `run_transaction` call that gets users in a particular city as a list of dictionaries.

        Arguments:
            city {String} -- The users' region.
            city {String} -- The users' city.

        Returns:
            List -- A list of dictionaries containing user data.
        """
        return run_transaction(sessionmaker(bind=self.engine),
                               lambda session: get_users_txn(session, region, city))

    def get_user(self, username=None, user_id=None):
        """
        Wraps a `run_transaction` call that gets a User object. As a required function for LoginManager, the function must take the `user_id` argument, and return a User object.

        Keyword Arguments:
            username {String} -- The user's username. (default: {None})
            user_id {UUID} -- The user's unique ID. (default: {None})

        Returns:
            User -- A User object.
        """
        return run_transaction(
            sessionmaker(bind=self.engine),
            lambda session: get_user_txn(session, username, user_id))

    def get_vehicles(self, region, city):
        """
        Wraps a `run_transaction` call that gets vehicles in a particular city as a list of dictionaries.

        Arguments:
            region {String} -- The vehicle's region.
            city {String} -- The vehicle's city.

        Returns:
            List -- A list of dictionaries containing vehicle data.
        """
        return run_transaction(sessionmaker(bind=self.engine),
                               lambda session: get_vehicles_txn(session, region, city))

    def get_rides(self, rider_id):
        """
        Wraps a `run_transaction` call that gets rides in a particular city as a list of dictionaries.

        Arguments:
            rider_id {UUID} -- The user's unique ID.

        Returns:
            List -- A list of dictionaries containing ride data.
        """
        return run_transaction(
            sessionmaker(bind=self.engine),
            lambda session: get_rides_txn(session, rider_id))
