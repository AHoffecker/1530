from flask import Flask, render_template, request
import os
from models import db, Restaurant, Review

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models.db'

# Bind the db to the app
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map_page')
def map_page():
    return render_template('map.html', google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY"))

@app.route('/view_wait')
def view_wait():
    return render_template('view_wait.html')
    
@app.route('/review')
def review():
    return render_template('review.html')