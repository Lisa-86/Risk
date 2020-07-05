from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from models import *
from db import db
from territories import territories

web = Blueprint('main', __name__)

@web.route('/')
@login_required
def home():
    return render_template("home.html")

@web.route('/profile')
@login_required
def profile():
   return render_template("profile.html", name = current_user.name)

@web.route('/test')
def test():
    ter = Territory.query.filter_by(country='Eastern Australia').first()
    return str(ter.neighbours)

@web.route('/populate')
def populate():
    # remove all the territories first
    for ter in Territory.query.all():
        db.session.delete(ter)
    db.session.commit()

    # create users
    prev_mat = User.query.filter_by(name='mat').first()
    prev_lisa = User.query.filter_by(name='lisa').first()
    if prev_mat is not None:
        db.session.delete(prev_mat)
    if prev_lisa is not None:
        db.session.delete(prev_lisa)
    db.session.commit()
    mat = User(email="bieniekmat@gmail.com", name="mat", password=generate_password_hash("risk12", method='sha256'))
    lis = User(email="pod.features@gmail.com", name="lisa", password=generate_password_hash("risk12", method='sha256'))
    db.session.add(mat)
    db.session.add(lis)
    db.session.commit()

    # create the territories in the database
    for ter, values in territories.items():
        db_ter = Territory(country=ter, locx=values['loc'][0], locy=values['loc'][1])
        db.session.add(db_ter)
    db.session.commit()
    # add the neighbours
    for ter, values in territories.items():
        from_ter = Territory.query.filter_by(country=ter).first()
        for neighbour in values['neighbours']:
            to_ter = Territory.query.filter_by(country=neighbour).first()
            from_ter.neighbours.append(to_ter)
        db.session.add(from_ter)
        db.session.commit()

    return redirect(url_for('auth.login'))