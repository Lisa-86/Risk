from flask import Flask, render_template, session
from flask_restful import Resource, Api
import random
from territories import teralloc, territories

app = Flask(__name__)
api = Api(app)
risk_data = {}

@app.route('/')
def run_risk():
    return render_template("home.html")

class TroopResource(Resource):
    def get(self):
        if 'territories' in risk_data:
            # get the current state of play
            return risk_data['territories']
        else:
            # allocate territories and initial troops to players
            allocated_ters = teralloc(territories)
            risk_data['territories'] = allocated_ters
            return allocated_ters

class PlayerTurn(Resource):
    def get(self):
        if 'whichPlayer' in risk_data:
            return risk_data['whichPlayer']
        # decide who goes first
        risk_data['whichPlayer'] = random.randint(1, 2) # only between two player for now
        return risk_data['whichPlayer']


api.add_resource(TroopResource, '/countries')
api.add_resource(PlayerTurn, '/REST/player')

if __name__ == '__main__':
    app.run()
