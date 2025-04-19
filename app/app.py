from flask import Flask, render_template, request
import os
from models import db, Restaurant, Review

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models.db'

# Bind the db to the app
db.init_app(app)

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
    max_wait = request.form.get('maxWaitTime', type=int)

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