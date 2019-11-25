from cockroachdb.sqlalchemy import run_transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import registry
registry.register("cockroachdb", "cockroachdb.sqlalchemy.dialect", "CockroachDBDialect")
from movr.transactions import start_ride_txn, end_ride_txn, add_user_txn, add_vehicle_txn, get_users_txn, get_user_txn, get_vehicles_txn, get_rides_txn, remove_user_txn, remove_vehicle_txn

class MovR:
    def __init__(self, conn_string, echo = False):
        self.engine = create_engine(conn_string, convert_unicode=True, echo=echo)
        self.session = sessionmaker(bind=self.engine, expire_on_commit=False)()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()


    def start_ride(self, city, rider_id, rider_city, vehicle_id):
        return run_transaction(sessionmaker(bind=self.engine), lambda session: start_ride_txn(session, city, rider_id, rider_city, vehicle_id))


    def end_ride(self, city, ride_id, location):
        return run_transaction(sessionmaker(bind=self.engine), lambda session: end_ride_txn(session, city, ride_id, location))


    def add_user(self, city, first_name, last_name, email, username, password):
        return run_transaction(sessionmaker(bind=self.engine), lambda session: add_user_txn(session, city, first_name, last_name, email, username, password))


    def remove_user(self, city, user_id):
        return run_transaction(sessionmaker(bind=self.engine), lambda session: remove_user_txn(session, city, user_id))


    def remove_vehicle(self, city, vehicle_id):
        return run_transaction(sessionmaker(bind=self.engine), lambda session: remove_vehicle_txn(session, city, vehicle_id))


    def add_vehicle(self, city, owner_id, last_location, type, color, brand, status, is_owner=False):
        return run_transaction(sessionmaker(bind=self.engine), lambda session: add_vehicle_txn(session, city, owner_id, last_location, type, color, brand, status, is_owner))


    def get_users(self, city):
        return run_transaction(sessionmaker(bind=self.engine), lambda session: get_users_txn(session, city))


    def get_user(self, username=None, user_id=None):
        return run_transaction(sessionmaker(bind=self.engine), lambda session: get_user_txn(session, username, user_id))


    def get_vehicles(self, city):
        return run_transaction(sessionmaker(bind=self.engine), lambda session: get_vehicles_txn(session, city))


    def get_rides(self, rider_id):
        return run_transaction(sessionmaker(bind=self.engine), lambda session: get_rides_txn(session, rider_id))

