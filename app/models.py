from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# Initialize db object
db = SQLAlchemy()

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    phoneNumber = db.Column(db.String(10))
    emailAddress = db.Column(db.String(120))
    address = db.Column(db.String(200))
    menu = db.Column(db.Text)
    openTime = db.Column(db.Time)  # corrected
    closeTime = db.Column(db.Time)  # corrected
    paymentMethods = db.Column(db.Text)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    rating = db.Column(db.SmallInteger, nullable=False)  # corrected
    writtenReview = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    restaurant = db.relationship('Restaurant', backref=db.backref('reviews', lazy=True))

class WaitTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    lengthOfWait = db.Column(db.Integer, nullable=False)
    orderTime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))   # ⬅️ FIXED
    receivedTime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) # ⬅️ FIXED
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))    # ⬅️ FIXED
