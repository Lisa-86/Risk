from flask_login import UserMixin

from db import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    player2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    currentPlayer = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

class Neighbours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TerFromId = db.Column(db.Integer, db.ForeignKey('territory.id'))
    TerToId = db.Column(db.Integer, db.ForeignKey('territory.id'))

class Territory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    locX = db.Column(db.Integer)
    locY = db.Column(db.Integer)

class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    territoryId = db.Column(db.Integer, db.ForeignKey('territory.id'))
    troopNo = db.Column(db.Integer)
    currentOwner = db.Column(db.Integer, db.ForeignKey('user.id'))
