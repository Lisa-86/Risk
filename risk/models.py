from flask_login import UserMixin, current_user
import sqlalchemy

from .db import db
from sqlalchemy import func


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
    startDate = db.Column(db.DateTime, nullable=False)
    player1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player1 = db.relationship('User', backref=db.backref("games1", uselist=True), uselist=False,
                              primaryjoin=player1_id == User.id)
    player2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    player2 = db.relationship('User', backref=db.backref("games2", uselist=True), uselist=False,
                              primaryjoin=player2_id == User.id)

    currentPlayerId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    stage = db.Column(db.String(20))
    territories = db.relationship('GameState', backref='game', lazy=False)
    # reinforcement information, number, terFrom and terTo
    reinNo = db.Column(db.Integer, nullable = True)
    reinFrom = db.Column(db.Integer, db.ForeignKey('territory.id'), nullable = True)
    reinTo = db.Column(db.Integer, db.ForeignKey('territory.id'), nullable = True)


class GameInvitation(db.Model):
    """
    Contains the invitee and inviter of games which haven't started yet
    """
    id = db.Column(db.Integer, primary_key=True)
    inviter = db.Column(db.Integer, db.ForeignKey('user.id'))
    invitee = db.Column(db.Integer, db.ForeignKey('user.id'))


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
    locx = db.Column(db.Integer)
    locy = db.Column(db.Integer)
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
    territory = db.relationship('Territory', uselist=False, primaryjoin=territoryId==Territory.id)
    troopNo = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id', ondelete="cascade"), nullable=False)
