from flask import Flask, render_template, request
import os
from models import db, Restaurant, Review, WaitTime
from sqlalchemy import func

# Initialize Flask app
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models.db'  # Adjust for your DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to suppress a warning

# Bind the db to the app
db.init_app(app)

# Function to add the list of restaurants
def add_restaurants():
    restaurants = [
        "Auntie Anne's", "Burrito Bowl", "Cafe 1923", "Campus Coffee & Tea Co - Sutherland", 
        "Campus Coffee & Tea Co - Towers", "Cathedral Sushi", "Chick-fil-A", "CrEATe", 
        "Ft. Pitt Subs", "PA Taco Co.", "Pom & Honey", "Shake Smart", "Steel City Kitchen", 
        "The Delicatessen", "The Eatery", "The Perch", "The Roost", "True Burger", "Wicked Pie"
    ]
    
    for name in restaurants:
        # Check if the restaurant already exists to avoid duplicates
        if not Restaurant.query.filter_by(name=name).first():
            restaurant = Restaurant(
                name=name,
                phoneNumber=None,
                emailAddress=None,
                address=None,
                menu=None,
                openTime=None,
                closeTime=None,
                paymentMethods=None,
                username=None,
                password=None
            )
            db.session.add(restaurant)
    
    db.session.commit()

# Create tables if they do not exist (done once when the app starts up)
with app.app_context():
    db.create_all()  # Creates the tables in the database if they do not exist
    add_restaurants()  # Add the list of restaurants to the database

@app.route('/')
def home():
    return render_template('map.html')

@app.route('/map_page')
def map_page():
    return render_template('map.html', google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY"))

@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')

@app.route('/search_results', methods=['POST'])
def search_results():
    max_wait = request.form.get('waitTime', type=int)

    if max_wait is not None:
        # Calculate the average wait time for each restaurant
        avg_wait_times = db.session.query(
            WaitTime.restaurant_id,
            func.avg(WaitTime.lengthOfWait).label('avg_wait')
        ).group_by(WaitTime.restaurant_id).subquery()

        # Join Restaurant and the average wait times to get restaurant names
        restaurants_with_avg_wait = db.session.query(
            Restaurant.name,
            avg_wait_times.c.avg_wait
        ).join(
            avg_wait_times, Restaurant.id == avg_wait_times.c.restaurant_id
        ).filter(
            avg_wait_times.c.avg_wait <= max_wait
        ).all()

        return render_template('search_results.html', max_wait=max_wait, restaurants=restaurants_with_avg_wait)
    else:
        return render_template('search_results.html', error="Please enter a valid maximum wait time.")

@app.route('/review')
def review():
    return render_template('review.html')

if __name__ == '__main__':
    app.run(debug=True)
