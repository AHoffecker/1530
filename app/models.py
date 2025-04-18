from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    phoneNumber = db.Column(db.String(10), unique=True, nullable=False)
    emailAddress = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    menu = db.Column(db.Text)
    openTime = db.Column(db.models.TimeField(_(""), auto_now=False, auto_now_add=False))
    closeTime = db.Column(db.models.TimeField(_(""), auto_now=False, auto_now_add=False))
    paymentMethods = db.Column(db.Text)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
                         

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    rating = db.Column(db.models.SmallIntegerField(_("")))
    writtenReview = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    restaurant = db.relationship('Restaurant', backref=db.backref('reviews', lazy=True))

    
class WaitTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    lengthOfWait = db.Column(db.Integer, nullable=False)
    orderTime = db.column(db.timestamp, default=datetime.utcnow)
    receivedTime = db.column(db.timestamp, default=datetime.utcnow)
    timestamp = db.Column(db.timestamp, default=datetime.utcnow)
    