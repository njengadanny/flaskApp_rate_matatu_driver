from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from . import db
from flask_login import logout_user, login_user, login_required, current_user, LoginManager
import random
import string

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/admin')
def admin():
    return render_template('admin.html', values=User.query.all())

@auth.route('/admin_login')
def admin_log():
    return render_template('admin_login.html')

@auth.route('/admin_login', methods=['POST'])
def admin_login():
    email = 'admin@mail.com'
    password = 'admin'

    admin = User.query.filter_by(email=email).first()

    # check if the user exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if admin:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.admin_login')) # if the user doesn't exist or password is wrong, reload the page
    
    # if the above check passes, then we know the user has the right credentials    
    # login_user(admin)

    # login code goes here
    return redirect(url_for('auth.admin'))

@auth.route('/matatu_register')
def matatu_details():
    return render_template('matatu_register.html', values=Matatu.query.all())

@auth.route('/matatu_register', methods=['POST'])
def matatu_register():
    matatu_plate_no = request.form.get('matatu_plate_no')    
    matatu_model = request.form.get('matatu_model')
    owner_name = request.form.get('owner_name')
    
    matatu = Matatu.query.filter_by(matatu_plate_no=matatu_plate_no).first()
    
    if matatu:
        flash('Matatu Exists.')
        return redirect(url_for('auth.matatu_register'))
    
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_matatu = Matatu(matatu_plate_no=matatu_plate_no, matatu_model=matatu_model, owner_name=owner_name)
    
    #add new driver to database
    db.session.add(new_matatu)
    db.session.commit()
    
    #code to validate and add user to database goes here
    return redirect(url_for('auth.admin')) #TODO: modify auth.admin to a page showing driver details


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user: # if a user is found, redirect back to signup page so user can try again
        flash('These credentials exist')
        return redirect(url_for('auth.signup'))
    
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, fname=fname, lname=lname, password=generate_password_hash(password, method='sha256'))
    
    #add new user to database
    db.session.add(new_user)
    db.session.commit()
    
    #code to validate and add user to database goes here
    return redirect(url_for('auth.login')) 

@auth.route('/login', methods=['POST'])
def login_post():    
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    
    # if the above check passes, then we know the user has the right credentials    
    login_user(user, remember=remember)

    # login code goes here
    return redirect(url_for('main.profile'))

@auth.route('/driver_profile')
# @login_required
def driver_profile():
    return render_template('driver_profile.html', 
    driver_fname=current_user.driver_fname, driver_lname=current_user.driver_lname, driver_email=current_user.driver_email,
    driver_phone_num=current_user.driver_phone_num, rating=current_user.avg_rating)

@auth.route('/driver_login')
def driver_login():       
    return render_template('driver_login.html', values=Driver.query.filter(Driver.avg_rating))

@auth.route('/driver_signup')
def driver_signup():
    return render_template('driver_signup.html', values=Driver.query.filter(Driver.avg_rating>=4.5))

@auth.route('/driver_signup', methods=['POST'])
def driver_register():
    driver_phone_num = request.form.get('driver_phone_num')    
    driver_fname = request.form.get('driver_fname')
    driver_lname = request.form.get('driver_lname')
    driver_email = request.form.get('driver_email')
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(6))
    
    print(password)
    driver = Driver.query.filter_by(driver_phone_num=driver_phone_num).first()
    
    if driver:
        flash('Driver Exists.')
        return redirect(url_for('auth.driver_signup'))
    
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_driver = Driver(driver_phone_num=driver_phone_num, driver_fname=driver_fname, driver_lname=driver_lname, driver_email=driver_email, password=generate_password_hash(password, method='sha256'))
    
    #add new driver to database
    db.session.add(new_driver)
    db.session.commit()
    
    return redirect(url_for('auth.driver_login')) #TODO: modify auth.admin to a page showing driver details
    
@auth.route('/driver_login', methods=['POST'])
def login_driver():
    driver_email = request.form.get('driver_email')   
    password = request.form.get('password')#todo: hash password
    remember = True if request.form.get('remember') else False

    driver = Driver.query.filter_by(driver_email=driver_email).first()
    
     
    if not driver:
        flash('Incorrect Credentials!')
        return redirect(url_for('auth.driver_login'))
    
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    login_user(driver, remember=remember)       
    
    #code to validate and add user to database goes here
    return redirect(url_for('auth.driver_profile')) #TODO: modify auth.admin to a page showing driver details


