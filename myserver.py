
import random
import sys

from flask import Flask, render_template, session
from flask_login import LoginManager
from flask_restful import Resource, Api

from territories import teralloc, territories
from risk import reinforcements, diceroll, winGame
from db import db
from models import User
from auth import auth as auth_blueprint
from main import main as main_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'gcfgxdfszrt2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# add other URLs etc
app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)

api = Api(app)

risk_data = {} # keys: currentPlayer, territories, stage
# defines the clickable square around the number
# these values are relative to the map size
risk_data['tolerance'] = 0.02
risk_data['factorX'] = 0.015
risk_data['factorY'] = -0.015

# stages: DEPLOY, REINFORCE, ATTACK, MANOEUVRE, FINAL_MAN, WIN!

class TroopResource(Resource):
    """
        1. Allocate territories
        2. Set the stage to reinforcment
    """
    def get(self):
        if 'territories' in risk_data:
            # get the current state of play
            return risk_data
        else:
            # allocate territories and initial troops to players
            allocated_ters = teralloc(territories, testWin=True)
            risk_data['territories'] = allocated_ters
            risk_data['stage'] = "DEPLOYMENT"

            # decide who goes first
            risk_data['currentPlayer'] = random.randint(1, 2)  # only between two player for now
            # and how many reinforcements the first time
            risk_data['reinNo'] = reinforcements(risk_data['territories'], risk_data['currentPlayer'])

            return risk_data


class Deployment(Resource):
    def put(self, country):
        risk_data['territories'][country]['troopNo'] += 1
        # update the number of available reinforcment troops
        risk_data['reinNo'] -= 1
        if risk_data['reinNo'] == 0:
            risk_data['stage'] = 'ATTACK'
        return risk_data


class Diceroll(Resource):
    def put(self, terFrom, terTo):
        attTroops = risk_data['territories'][terFrom]['troopNo']
        defTroops = risk_data['territories'][terTo]['troopNo']
        outcomeAtt, outcomeDef = diceroll(attTroops,defTroops)
        risk_data['territories'][terFrom]['troopNo'] = outcomeAtt
        risk_data['territories'][terTo]['troopNo'] = outcomeDef
        if (outcomeDef == 0):
            risk_data['territories'][terTo]['playerNo'] = risk_data['currentPlayer']
            risk_data['territories'][terTo]['troopNo'] = 1
            risk_data['territories'][terFrom]['troopNo'] -= 1
            risk_data['stage'] = 'REINFORCE'
            risk_data['reinFrom'] = terFrom
            risk_data['reinTo'] = terTo
        return risk_data


class Reinforcement(Resource):
    def put(self, input):
        terFrom = risk_data['reinFrom']
        terTo = risk_data['reinTo']
        risk_data['territories'][terFrom]['troopNo'] -= input
        risk_data['territories'][terTo]['troopNo'] += input
        risk_data['stage'] = "ATTACK"
        return risk_data


class EndMove(Resource):
    def put(self):
        risk_data["stage"] = "MANOEUVRE"
        return risk_data


class Man(Resource):
    def put(self, terFrom, terTo, troopNo):
        risk_data['territories'][terFrom]['troopNo'] -= troopNo
        risk_data['territories'][terTo]['troopNo'] += troopNo

        if risk_data['currentPlayer'] == 1:
            risk_data['currentPlayer'] = 2
        else:
            risk_data['currentPlayer'] = 1

        risk_data['stage'] = "DEPLOYMENT"
        risk_data['reinNo'] = reinforcements(risk_data['territories'], risk_data['currentPlayer'])

        return risk_data


class EndTurn(Resource):
    def put(self):
        winCheck = winGame(risk_data)

        if winCheck == True:
            return risk_data

        else:
            if risk_data['currentPlayer'] == 1:
                risk_data['currentPlayer'] = 2
            else:
                risk_data['currentPlayer'] = 1

            risk_data['stage'] = "DEPLOYMENT"
            risk_data['reinNo'] = reinforcements(risk_data['territories'], risk_data['currentPlayer'])

            return risk_data



api.add_resource(TroopResource, '/REST/countries')
api.add_resource(Deployment, '/REST/deployment/<string:country>')
api.add_resource(Diceroll, '/REST/diceroll/<string:terFrom>/<string:terTo>')
api.add_resource(Reinforcement, '/REST/reinforcement/<int:input>')
api.add_resource(EndMove, '/REST/endmove')
api.add_resource(Man, '/REST/man/<string:terFrom>/<string:terTo>/<int:troopNo>')
api.add_resource(EndTurn, '/REST/endTurn')

# Just do this once: Create the database file
# db.create_all(app=app)
# sys.exit()

if __name__ == '__main__':
    app.run()
