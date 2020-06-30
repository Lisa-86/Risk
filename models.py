from flask_login import UserMixin
from db import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Game(db.Model):
    """
    Metadata about the game.
    """
    id = db.Column(db.Integer, primary_key=True)
    player1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    player2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    currentPlayer = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    states = db.relationship('GameState', backref='game', lazy=False)

neighbours = db.Table("neighbours",
    db.Column('terFrom', db.Integer, db.ForeignKey('territory.id'), primary_key=True),
    db.Column('terTo', db.Integer, db.ForeignKey('territory.id'), primary_key=True)
)

class Territory(db.Model):
    """
    Unique list of territories
    """
    __tablename__ = 'territory'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    locX = db.Column(db.Integer)
    locY = db.Column(db.Integer)
    neighbours = db.relationship("Territory",
                               secondary=neighbours,
                               primaryjoin=id == neighbours.c.terFrom,
                               secondaryjoin=id == neighbours.c.terTo,
                                 )# backref="left_nodes")

    def __repr__(self):
        return f'Territory {self.country}'


class GameState(db.Model):
    """
    For each game for each territory contains information about who owns it with how many troops
    """
    id = db.Column(db.Integer, primary_key=True)
    territoryId = db.Column(db.Integer, db.ForeignKey('territory.id'))
    troopNo = db.Column(db.Integer)
    currentOwner = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
