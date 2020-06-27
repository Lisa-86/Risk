from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def run_risk():
    return render_template("home.html")

@main.route('/profile')
@login_required
def profile():
   return render_template("profile.html", name = current_user.name)

@main.route('/base')
def base():
    return render_template("base.html")