from flask import Blueprint, render_template, request
from . import db
from flask_login import login_required, current_user
from .models import *
from datetime import datetime

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/performing')
def performing():
    return render_template('performing.html', values=Driver.query.filter(Driver.avg_rating>=4.5))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', fname=current_user.fname, lname=current_user.lname, email=current_user.email)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/after_rating')
def after_rating():
    return render_template('after_rating.html')

@main.route('/feedback')
@login_required
def feedback():
    return render_template('feedback.html', options=Driver.query.with_entities(Driver.id), values=Ratings.query.all())

nltk.download('stopwords')

set(stopwords.words('english'))

@main.route('/feedback', methods=['POST'])
def analyze():
    comment = request.form.get('review')
    star_rating = request.form['star']
    date_time = datetime.now
    email = current_user.email
    driver_id = request.form.get('driver_id')
    
    options = Driver.query.with_entities(Driver.id)
    
    stop_words = stopwords.words('english')
    review = request.form['review'].lower()

    processed_doc1 = ' '.join([word for word in review.split() if word not in stop_words])

    sa = SentimentIntensityAnalyzer()
    dd = sa.polarity_scores(text=processed_doc1)
    compound = round((1 + dd['compound'])/2, 2)
    
    new_rating = Ratings(star_rating=star_rating, comment=comment, email=email, driver_id=driver_id, positivity=compound)
   
    #add new comment to database
    db.session.add(new_rating)
    db.session.commit()
        
    return render_template('feedback.html', final=compound, review=review, options=options)
