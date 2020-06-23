from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def run_risk():
    return render_template("home.html")

@main.route('/profile')
def profile():
   return render_template("profile.html")

@main.route('/base')
def base():
    return render_template("base.html")
