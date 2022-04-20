from . import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import orm
from sqlalchemy.sql import func
from sqlalchemy_utils import aggregated
from sqlalchemy.schema import Sequence
from sqlalchemy import event
from sqlalchemy import DDL

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(1000)) 
    lname = db.Column(db.String(1000)) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    
    
class Matatu(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    matatu_plate_no = db.Column(db.String(100), unique=True)
    matatu_model = db.Column(db.String(1000))
    owner_name = db.Column(db.String(1000))
    
class Driver(db.Model, UserMixin):    
    id = db.Column(db.Integer, primary_key=True)
    driver_phone_num = db.Column(db.Integer, unique=True)
    driver_fname = db.Column(db.String(1000))
    driver_lname = db.Column(db.String(1000))
    driver_email = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(100))
    ratings = db.Column(db.SmallInteger)
    
    @aggregated('ratings', db.Column(db.SmallInteger))
    def avg_rating(self):
        return db.func.avg(Ratings.star_rating)

    ratings = orm.relationship('Ratings')

    
class Ratings(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    star_rating = db.Column(db.SmallInteger)
    comment = db.Column(db.String(1000))
    email = db.Column(db.String(100), db.ForeignKey('user.email', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    driver_id = db.Column(db.String(100), db.ForeignKey('driver.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    positivity = db.Column(db.Integer)
    