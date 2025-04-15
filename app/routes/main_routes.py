from flask import Blueprint, render_template
import os

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/map_page')
def map_page():
    return render_template('map.html', google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY"))

@main.route('/view_wait')
def view_wait():
    return render_template('view_wait.html')
    
@main.route('/review')
def review():
    return render_template('review.html')
