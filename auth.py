from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # check email field isn't empty
    if email == "":
        flash('Must provide an email address')
        return redirect(url_for('auth.signup'))

    # check name field isn't empty
    if name == "":
        flash('Must provide a username')
        return redirect(url_for('auth.signup'))

    # check password field isn't empty
    if password == "":
        flash('Must provide a password')
        return redirect(url_for('auth.signup'))

    # check if password is minimum 6 characters
    if len(password) < 6:
        flash('Password must be minimum of 6 characters long')
        return redirect(url_for('auth.signup'))

    # check if password is secure
    # TODO

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))


    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    # check if user exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials


    return redirect(url_for('main.profile'))


@auth.route('/logout')
def logout():
    return "logout"