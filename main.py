
import random
import sys

from flask import Flask, render_template, session
from flask_login import LoginManager, current_user
from flask_restful import Resource, Api

from territories import teralloc, teralloc_db, territories
from risk import reinforcements_db, diceroll, winGame
from db import db
from models import *
from auth import auth as auth_blueprint
from web import web as main_blueprint
from rest import register_rest_api


def create_app(db_path):
    import logging
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gcfgxdfszrt2'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
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
    register_rest_api(app)

    # Just do this once: Create the database file
    db.create_all(app=app)

    return app


if __name__ == '__main__':
    app = create_app('sqlite:///db.sqlite')

    if sys.argv[-1] == 'waitress':
        # run waitress
        from waitress import serve
        serve(app, listen='*:80')
    else:
        # run typical flask
        app.run()