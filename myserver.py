
import random
import sys

from flask import Flask, render_template, session
from flask_login import LoginManager, current_user
from flask_restful import Resource, Api

from territories import teralloc, teralloc_db, territories
from risk import reinforcements, reinforcements_db, diceroll, winGame
from db import db
from models import *
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

# stages: DEPLOY, REINFORCE, ATTACK, MANOEUVRE, FINAL_MAN, WIN!

risk_data = {} # keys: currentPlayer, territories, stage
# defines the clickable square around the number
# these values are relative to the map size
risk_data['tolerance'] = 0.02
risk_data['factorX'] = 0.015
risk_data['factorY'] = -0.015

class TroopResource(Resource):
    """
        1. Allocate territories
        2. Set the stage to reinforcment
    """
    def get(self):
        if 'territories' in risk_data and False:
            # get the current state of play
            return risk_data
        else:
            # A NEW GAME
            # create a new game
            mat = User.query.filter_by(email='bieniekmat@gmail.com').first()
            lis = User.query.filter_by(email='pod.features@gmail.com').first()
            # decide who goes first
            current_player = random.sample([mat, lis], 1)[0]
            # create a game in the database
            game = Game(player1=mat.id, player2=lis.id, currentPlayer=current_player.id, stage='DEPLOYMENT')
            db.session.add(game)
            db.session.commit()

            # for each territory, create a gamestate
            game_states = []
            for ter in Territory.query.all():
                game_state = GameState(territoryId=ter.id, game_id=game.id)
                game_states.append(game_state)

            # allocate territories and initial troops to players
            teralloc_db(game_states, [mat, lis])

            # compute the reinforcement number
            game.reinNo = reinforcements_db(game_states, current_player)

            db.session.add(game)
            [db.session.add(gs) for gs in game_states]
            db.session.commit()

            game_json_ready = game.get_risk_json()
            game_with_meta = {**game_json_ready, **risk_data}
            return game_with_meta


class Deployment(Resource):
    def put(self, gameID, country):
        game = Game.query.filter_by(id=gameID).first()
        country_meta = Territory.query.filter_by(country=country).first()
        game_state = GameState.query.filter_by(game_id=game.id, territoryId=country_meta.id).first()

        # fixme: check if the game actually belongs to the player

        # check if the country belongs to the person
        # if game_state.owner != current_user.id:
        #     return "wowowowo, nice try hacker: you are not the current user in this game. "

        if not game.reinNo > 0:
            return "hohohoho, no way: you have no troops to deploy any more. "

        game_state.troopNo += 1
        # update the number of available reinforcment troops
        game.reinNo -= 1
        if game.reinNo == 0:
            game.stage = 'ATTACK'
        db.session.add(game_state)
        db.session.add(game)
        db.session.commit()

        game_json_ready = game.get_risk_json()
        game_with_meta = {**game_json_ready, **risk_data}
        return game_with_meta


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

api = Api(app)
api.add_resource(TroopResource, '/REST/countries')
api.add_resource(Deployment, '/REST/deployment/<int:gameID>/<string:country>')
api.add_resource(Diceroll, '/REST/diceroll/<string:terFrom>/<string:terTo>')
api.add_resource(Reinforcement, '/REST/reinforcement/<int:input>')
api.add_resource(EndMove, '/REST/endmove')
api.add_resource(Man, '/REST/man/<string:terFrom>/<string:terTo>/<int:troopNo>')
api.add_resource(EndTurn, '/REST/endTurn')

# Just do this once: Create the database file
db.create_all(app=app)

if __name__ == '__main__':
    app.run()
