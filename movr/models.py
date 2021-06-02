# START front
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Boolean, Interval, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.types import DATE
from sqlalchemy.dialects.postgresql import UUID
import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

Base = declarative_base()
# END front

# START User
class User(Base, UserMixin):
    """
    Represents rows of the users table.

    Arguments:
        Base {DeclaritiveMeta} -- Base class for declarative SQLAlchemy class definitions that produces appropriate `sqlalchemy.schema.Table` objects.
        UserMixin {UserMixin} -- Mixin object that provides default implementations for the methods that Flask-Login expects user objects to have.

    Returns:
        User -- Instance of the User class.
    """
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True)
    city = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    username = Column(String, unique=True)
    password_hash = Column(String)
    is_owner = Column(Boolean)

    def set_password(self, password):
        """
        Hash the password set by the user at registration.
        """
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return "<User(city='{0}', id='{1}', name='{2}')>".format(
            self.city, self.id, self.first_name + ' ' + self.last_name)
# END User


# START Vehicle
class Vehicle(Base):
    """
    Represents rows of the vehicles table.

    Arguments:
        Base {DeclaritiveMeta} -- Base class for declarative SQLAlchemy class definitions that produces appropriate `sqlalchemy.schema.Table` objects.

    Returns:
        Vehicle -- Instance of the Vehicle class.
    """
    __tablename__ = 'vehicles'
    id = Column(UUID, primary_key=True)
    city = Column(String)
    type = Column(String)
    owner_id = Column(UUID, ForeignKey('users.id'))
    date_added = Column(DATE, default=datetime.date.today)
    status = Column(String)
    last_location = Column(String)
    color = Column(String)
    brand = Column(String)

    def __repr__(self):
        return "<Vehicle(city='{0}', id='{1}', type='{2}', status='{3}')>".format(
            self.city, self.id, self.type, self.status)
# END Vehicle


# START Ride
class Ride(Base):
    """
    Represents rows of the rides table.

    Arguments:
        Base {DeclaritiveMeta} -- Base class for declarative SQLAlchemy class definitions that produces appropriate `sqlalchemy.schema.Table` objects.

    Returns:
        Ride -- Instance of the Ride class.
    """
    __tablename__ = 'rides'
    id = Column(UUID, primary_key=True)
    city = Column(String, ForeignKey('vehicles.city'))
    rider_id = Column(UUID, ForeignKey('users.id'))
    vehicle_id = Column(UUID, ForeignKey('vehicles.id'))
    start_location = Column(String)
    end_location = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    length = Column(Interval)

    def __repr__(self):
        return "<Ride(city='{0}', id='{1}', rider_id='{2}', vehicle_id='{3}')>".format(
            self.city, self.id, self.rider_id, self.vehicle_id)
# END Ride
