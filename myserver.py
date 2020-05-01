from flask import Flask, render_template, session
from flask_restful import Resource, Api
import random
from territories import teralloc, territories
from risk import reinforcements, diceroll

app = Flask(__name__)
api = Api(app)

risk_data = {} # keys: currentPlayer, territories, stage
# defines the clickable square around the number
# these values are relative to the map size
risk_data['tolerance'] = 0.02
risk_data['factorX'] = 0.015
risk_data['factorY'] = -0.015

# stages: DEPLOY, REINFORCE, ATTACK, MANOEUVRE, FINAL_MAN

@app.route('/')
def run_risk():
    return render_template("home.html")

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
            allocated_ters = teralloc(territories)
            risk_data['territories'] = allocated_ters
            risk_data['stage'] = "REINFORCE"

            # decide who goes first
            risk_data['currentPlayer'] = random.randint(1, 2)  # only between two player for now
            # and how many reinforcements the first time
            risk_data['reinNo'] = reinforcements(risk_data['territories'], risk_data['currentPlayer'])

            return risk_data

class PlayerTurn(Resource):
    def get(self):
        if 'currentPlayer' in risk_data:
            return risk_data
        # decide who goes first
        risk_data['currentPlayer'] = random.randint(1, 2) # only between two player for now
        return risk_data

class Reinforce(Resource):
    """
        How many to troops the current player can reinforce
    """
    def get(self):
        if 'reinNo' in risk_data:
            # return the reinforcment number for the current player
            return risk_data
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
        return [outcomeAtt, outcomeDef]


api.add_resource(TroopResource, '/REST/countries')
api.add_resource(PlayerTurn, '/REST/player')
api.add_resource(Reinforce, '/REST/reinforce')
api.add_resource(Deployment, '/REST/deployment/<string:country>')
api.add_resource(Diceroll, '/REST/diceroll/<string:terFrom>/<string:terTo>')

if __name__ == '__main__':
    app.run()
