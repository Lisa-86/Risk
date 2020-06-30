from flask_login import UserMixin
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
    rein_no = db.Column(db.Integer)
    states = db.relationship('GameState', backref='game', lazy=False)

    risk = ['id', 'player1', 'player2', 'currentPlayer', 'stage', 'states']

    def get_basic_dict(self):
        """
        Return all the information
        :return:
        """
        # for each key,
        to_return = {}
        for key in Game.risk:
            value = self.__getattribute__(key)
            # if the value is more complex, such as another model, fetch that separately
            if type(value) is sqlalchemy.orm.collections.InstrumentedList:
                simple_list = []
                for item in value:
                    simple_list.append(item.get_basic_dict())
                to_return[key] = simple_list
            else:
                to_return[key] = value
        return to_return

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

    risk = ['id', 'country', 'locX', 'locY', 'neighbours']

    def get_basic_dict(self):
        risk_data = {}
        for key in Territory.risk:
            value = self.__getattribute__(key)
            if type(value) is sqlalchemy.orm.collections.InstrumentedList:
                # it is a list, in this case extract only the name strings
                value = [neigh.country for neigh in value]

            risk_data[key] = value
        return risk_data

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
    currentOwner = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

    risk = ['id', 'territory', 'troopNo', 'currentOwner']

    def get_basic_dict(self):
        risk_data = {}
        for key in GameState.risk:
            value = self.__getattribute__(key)
            if type(value) is Territory:
                value = value.get_basic_dict()

            risk_data[key] = value
        return risk_data