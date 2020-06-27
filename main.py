from flask import Blueprint, render_template
from flask_login import login_required, current_user
from db import db
from models import *
from territories import territories

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

@main.route('/populate')
def populate():
    # create the territories in the database
    for ter, values in territories.items():
        db_ter = Territory(country=ter, locX=values['loc'][0], locY=values['loc'][1])
        db.session.add(db_ter)
    db.session.commit()
    # add the neighbours
    for ter, values in territories.items():
        from_ter = Territory.query.filter_by(country=ter).first()
        for neighbour in values['neighbours']:
            to_ter = Territory.query.filter_by(country=neighbour).first()
            new_neigh = Neighbours(TerFromId=from_ter.id, TerToId=to_ter.id)
            db.session.add(new_neigh)
            db.session.commit()

    return ('populated')