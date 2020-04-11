from flask import Flask, render_template
from flask_restful import Resource, Api

from territories import teralloc, territories

app = Flask(__name__)
api = Api(app)


@app.route('/')
def run_risk():
    return render_template("home.html")


class TroopResource(Resource):
    def get(self):
        # allocate territories and initial troops to players
        allocated_ters = teralloc(territories)
        return allocated_ters


api.add_resource(TroopResource, '/countries')

if __name__ == '__main__':
    app.run()
