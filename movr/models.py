from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Index, String, DateTime, Integer, Boolean, Float, Interval, ForeignKey, CheckConstraint
from sqlalchemy.types import DECIMAL, DATE
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(UUID, default=str(uuid.uuid4()), primary_key=True)
    city = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    username = Column(String, unique=True)
    password_hash = Column(String)
    is_owner = Column(Boolean)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return "<User(city='%s', id='%s', name='%s')>" % (self.city, self.id, self.first_name + ' ' + self.last_name)


class Vehicle(Base):
    __tablename__ = 'vehicles'
    id = Column(UUID, default=str(uuid.uuid4()), primary_key=True)
    city = Column(String, primary_key=True)
    type = Column(String)
    owner_id = Column(UUID, ForeignKey('users.id'))
    date_added = Column(DATE, default=datetime.date.today)
    status = Column(String)
    last_location = Column(String)
    color = Column(String)
    brand = Column(String)

    def __repr__(self):
        return "<Vehicle(city='%s', id='%s', type='%s', status='%s')>" % (self.city, self.id, self.type, self.status)


class Ride(Base):
    __tablename__ = 'rides'
    id = Column(UUID, default=str(uuid.uuid4()), primary_key=True)
    city = Column(String, ForeignKey('vehicles.city'), primary_key=True)
    rider_id = Column(UUID, ForeignKey('users.id'))
    rider_city = Column(String, ForeignKey('users.city'))
    vehicle_id = Column(UUID, ForeignKey('vehicles.id'))
    start_location = Column(String)
    end_location = Column(String)
    start_time = Column(DateTime, default=datetime.datetime.now)
    end_time = Column(DateTime)
    length = Column(Interval)

    def __repr__(self):
        return "<Ride(city='%s', id='%s', rider_id='%s', vehicle_id='%s')>" % (self.city, self.id, self.rider_id, self.vehicle_id)

