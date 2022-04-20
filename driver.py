from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from . import db
from flask_login import logout_user, login_user, login_required

driver = Blueprint('driver', __name__)

@driver.route('/driver_profile')
@login_required
def driver_profile():
    return render_template('driver_profile.html', values=Driver.query.all())

@driver.route('/driver_login')
def driver_login():       
    return render_template('driver_login.html', values=Driver.query.filter(Driver.avg_rating))

@driver.roure('/driver_signup')
def driver_signup():
    return render_template('driver_signup.html', values=Driver.query.filter(Driver.avg_rating))

@driver.route('/driver_signup', methods=['POST'])
def driver_register():
    driver_phone_num = request.form.get('driver_phone_num')    
    driver_fname = request.form.get('driver_fname')
    driver_lname = request.form.get('driver_lname')
    driver_email = request.form.get('driver_email')   
    
    driver = Driver.query.filter_by(driver_phone_num=driver_phone_num).first()
    
    if driver:
        flash('Driver Exists.')
        return redirect(url_for('auth.driver_details'))
    
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_driver = Driver(driver_phone_num=driver_phone_num, driver_fname=driver_fname, driver_lname=driver_lname, driver_email=driver_email)
    
    #add new driver to database
    db.session.add(new_driver)
    db.session.commit()
    
    #code to validate and add user to database goes here
    return redirect(url_for('auth.admin')) #TODO: modify auth.admin to a page showing driver details

@driver.route('/driver_login', methods=['POST'])
def driver_login():
    driver_phone_num = request.form.get('driver_phone_num')    
    driver_fname = request.form.get('driver_fname')
    driver_lname = request.form.get('driver_lname')
    driver_email = request.form.get('driver_email')   
    
    driver = Driver.query.filter_by(driver_phone_num=driver_phone_num).first()
    
    if not driver:
        flash('Driver Exists.')
        return redirect(url_for('auth.driver_details'))
    
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    login_user(driver)       
    
    #code to validate and add user to database goes here
    return redirect(url_for('auth.admin')) #TODO: modify auth.admin to a page showing driver details


