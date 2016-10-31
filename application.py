from app import application
"""
Models page for website with each pillar and its attributes
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sweetOutdoors:wearefine@sweetoutdoorsdb.ckneyrny5ckj.us-west-2.rds.amazonaws.com:5432/sweetOutdoors'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#pylint:disable=invalid-name, too-many-arguments, too-few-public-methods, too-many-instance-attributes

class Park(db.Model):

    """Park class with initializer to document models"""
    __tablename__ = 'Parks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    price = db.Column(db.Float)
    opentime = db.Column(db.Integer)
    closetime = db.Column(db.Integer)
    website = db.Column(db.String(256))
    zipcode = db.Column(db.Integer)

    state_id = db.Column(db.Integer, db.ForeignKey('States.id'), nullable=True)

    # events = db.relationship('Events', backref='Parks', lazy='dynamic')
    # campgrounds_rel = db.relationship(
    #     'Campgrounds', backref='Parks', lazy='dynamic')

    def __init__(self, name, price, opentime, closetime, website,
                 zipcode, state_id):

        self.name = name
        self.price = price
        self.opentime = opentime
        self.closetime = closetime
        self.website = website
        self.zipcode = zipcode
	self.state_id = None

    def __repr__(self):
        return '<Park %r>' % self.name


class Event(db.Model):

    """Event class with initializer to document models"""
    __tablename__ = 'Events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    category = db.Column(db.String(256))
    startDate = db.Column(db.String(256))  # may need to change
    email = db.Column(db.String(256))
    url = db.Column(db.String(256))
    zipcode = db.Column(db.Integer)

    # park_id_fk = db.Column(db.Integer, db.ForeignKey('Parks.idnum'))
    state_id = db.Column(db.Integer, db.ForeignKey('States.id'), nullable=True)

    def __init__(self, name, category, startDate, email, url, zipcode):#,
              #   park_id_fk, state_id_fk):

        self.name = name
        self.category = category
        self.startDate = startDate
        self.email = email
        self.url = url
        self.zipcode = zipcode
#        self.park_id_fk = park_id_fk
	self.state_id = None

    def __repr__(self):
        return '<Event %r>' % self.name


class State(db.Model):

    """State class with initializer to document models"""
    __tablename__ = 'States'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    highestPoint = db.Column(db.String(256))
    population = db.Column(db.Integer)
    description = db.Column(db.String(2048))
    total_area = db.Column(db.Float)

    campgrounds = db.relationship('Campgrounds', backref='States', lazy='dynamic')
    parks = db.relationship('Park', backref='State', lazy='dynamic')
    events = db.relationship('Events', backref='States', lazy='dynamic')

    def __init__(self, name, highestPoint, population, description,
                 total_area):
        self.name = name
        self.highestPoint = highestPoint
        self.population = population
        self.description = description
        self.total_area = total_area
	self.parks = parks
	self.events = events
	self.campgrounds = campgrounds

    def __repr__(self):
        return '<State %r>' % self.name


class Campground(db.Model):

    """Campground class with initializer to document models"""
    __tablename__ = 'Campgrounds'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    electricity = db.Column(db.Boolean)
    water = db.Column(db.Boolean)
    sewer = db.Column(db.Boolean)
    pets = db.Column(db.Boolean)

    # park_id_fk = db.Column(db.Integer, db.ForeignKey('Parks.idnum'))
    state_id = db.Column(db.Integer, db.ForeignKey('States.idnum'), nullable=True)

    def __init__(self, name, latitude, longitude, electricity, water,
                 sewer, pets):#, park_id_fk, state_id_fk):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.electricity = electricity
        self.water = water
        self.sewer = sewer
        self.pets = pets
        #self.park_id_fk = park_id_fk
        self.state_id = None

    def __repr__(self):
        return '<Campgrounds %r>' % self.name

if __name__ == '__main__':
	application.debug = True
	application.run()
