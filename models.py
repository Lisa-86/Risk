from flask_login import UserMixin, current_user
import sqlalchemy

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
    stage = db.Column(db.String(20))
    territories = db.relationship('GameState', backref='game', lazy=False)
    # reinforcement information, number, terFrom and terTo
    reinNo = db.Column(db.Integer, nullable = True)
    reinFrom = db.Column(db.Integer, db.ForeignKey('territory.id'), nullable = True)
    reinTo = db.Column(db.Integer, db.ForeignKey('territory.id'), nullable = True)

    def get_risk_json(self):
        # prepare the game json for the client
        # gather the territories information
        risk_territories = {}
        for ter in self.territories:
            tername, tervalues = ter.get_risk_structure()
            risk_territories[tername] = tervalues

        # create a simple game dictionary
        game = {
            'id': self.id,
            'player1': self.player1,
            'player2': self.player2,
            'currentPlayer': self.currentPlayer,
            'stage': self.stage,
            'territories': risk_territories,
            'reinNo': self.reinNo,
            'myID': current_user.id,
        }
        return game


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
    territory = db.relationship('Territory', uselist=False)
    troopNo = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

    def get_risk_structure(self):
        # prepare the risk structure for the client json
        country_name = self.territory.country
        country_info = {
            # map info, loc x y, name, neighbours
            'locx': self.territory.locx,
            'locy': self.territory.locy,
            'neighbours': [neigh.country for neigh in self.territory.neighbours],
            # user/game data (who it belongs to etc)
            'troopNo': self.troopNo,
            'owner': self.owner,
            # to identify the game state internally
            'id': self.id
        }
        return country_name, country_info