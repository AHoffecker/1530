from flask import Flask, render_template, request, redirect, url_for, session
import os
import datetime
from models import db, Restaurant, Review, WaitTime
from sqlalchemy import func, asc
import random

# Initialize Flask app
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models.db'  # Adjust for your DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to suppress a warning
app.secret_key = 'our_secret_key'
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

def add_wait(r_id, lengthOfWait):
    waitTime = WaitTime(
        restaurant_id = r_id,
        lengthOfWait = lengthOfWait,
        orderTime = (datetime.datetime.now()-datetime.timedelta(seconds = lengthOfWait*60)).time(),
        receivedTime = datetime.datetime.now().time(),
        timestamp = datetime.datetime.now().time()
    )
    db.session.add(waitTime)
    db.session.commit()

def add_review(r_id, rating, writtenReview):
    review = Review(
        restaurant_id = r_id,
        rating = rating,
        writtenReview = writtenReview,
        timestamp = datetime.datetime.now().time(),
        restaurant = None # What does this do?
    )
    db.session.add(review)
    db.session.commit()

def add_fake_wait_data(): # Adds random fake data
    for _ in range(5):
        id = random.randint(0,20)
        wait = random.randint(0,100)
        add_wait(id, wait)

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
    time = request.form.get('time', type=str) # get time from search or search_results form
    max_wait = ''

    try: # turn time into int
        max_wait = int(time)
    except: # all wait times
        if time == "any":
            max_wait = "any"

    if max_wait is not None:
        # Calculate the average wait time for each restaurant
        avg_wait_times = db.session.query(
            WaitTime.restaurant_id,
            func.avg(WaitTime.lengthOfWait).label('avg_wait')
        ).group_by(WaitTime.restaurant_id).subquery()

        # Join Restaurant and the average wait times to get restaurant names
        if max_wait != "any":
            restaurants_with_avg_wait = db.session.query(
                Restaurant.name,
                func.ceil(func.cast(avg_wait_times.c.avg_wait, db.Integer))
            ).join(
                avg_wait_times, Restaurant.id == avg_wait_times.c.restaurant_id
            ).filter(
                avg_wait_times.c.avg_wait <= max_wait
            ).order_by(asc(avg_wait_times.c.avg_wait)
            ).all()
        else:
            restaurants_with_avg_wait = db.session.query(
                Restaurant.name,
                func.ceil(func.cast(avg_wait_times.c.avg_wait, db.Integer))
            ).join(
                avg_wait_times, Restaurant.id == avg_wait_times.c.restaurant_id
            ).order_by(asc(avg_wait_times.c.avg_wait))

        return render_template('search_results.html', max_wait=max_wait, restaurants=restaurants_with_avg_wait)
    else:
        return render_template('search_results.html', error="Please enter a valid maximum wait time.")

@app.route('/submit_wait', methods=['GET', 'POST'])
def submit_wait():
    if request.method == 'POST':
        restaurant_name = request.form['restaurant']
        wait_time = request.form.get('waitTime', type=int)

        restaurant = Restaurant.query.filter_by(name=restaurant_name).first()
        if restaurant and wait_time is not None:
            add_wait(restaurant.id, wait_time)
            session['review_restaurant_id'] = restaurant.id
            return redirect(url_for('ask_for_review'))

    restaurants = Restaurant.query.order_by(Restaurant.name).all()
    return render_template('submit_wait.html', restaurants=restaurants)

@app.route('/ask_for_review', methods=['GET'])
def ask_for_review():
    return render_template('ask_for_review.html')

@app.route('/submit_review', methods=['GET', 'POST'])
def submit_review():
    if request.method == 'POST':
        restaurant_id = session.get('review_restaurant_id')
        if restaurant_id:
            rating = request.form.get('rating', type=int)
            writtenReview = request.form.get('review')
            if rating and writtenReview:
                add_review(restaurant_id, rating, writtenReview)
        session.pop('review_restaurant_id', None)
        return redirect(url_for('home'))

    return render_template('review.html')

if __name__ == '__main__':
    app.run(debug=True)