from flask import Flask, render_template
from flask_restful import Resource, Api

from territories import teralloc, territories, ters

app = Flask(__name__)
api = Api(app)

@app.route('/')
def run_risk():
    return render_template("home.html")

class TroopResource(Resource):
    def get(self):
        p1ters, p2ters = teralloc(ters)
        return {'player 1 territories': p1ters, "player 2 territories": p2ters}

api.add_resource(TroopResource, '/countries')

if __name__ == '__main__':
    app.run()

