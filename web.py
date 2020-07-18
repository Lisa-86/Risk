from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import or_

from models import *
from db import db
from territories import territories

web = Blueprint('web', __name__)


@web.route('/')
@login_required
def home():
    # get all the ongoing games
    games_ongoing_first = Game.query.filter_by(player1 = current_user.id)
    games_ongoing_second = Game.query.filter_by(player2 = current_user.id)
    games_ongoing = set(list(games_ongoing_first) + list(games_ongoing_second))

    # get all games that you are invited for
    invited_to_games =  GameInvitation.query.filter_by(invitee=current_user.id).all()
    parsed_invited_to_games = []
    for p in invited_to_games:
        u = User.query.filter_by(id=p.inviter).first()
        parsed_invited_to_games.append(u)

    # get all the games we've invited other people to
    invited_others = GameInvitation.query.filter_by(inviter=current_user.id).all()
    parsed_invited_others = []
    for p in invited_others:
        u = User.query.filter_by(id=p.invitee).first()
        parsed_invited_others.append(u)

    return render_template("home.html", name = current_user.name,
                          games_invited_to = parsed_invited_to_games,
                           games_invited_other = parsed_invited_others,
                           games_ongoing = games_ongoing)

@web.route('/createGame')
@login_required
def createGame():
    return render_template("createGame.html")

@web.route('/createGame', methods=['POST'])
def createGamePost():
    email = request.form.get('email')

    # returns the whole user related to this email
    user = User.query.filter_by(email=email).first()

    # check if there is such a user, if not return error message
    if user is None:
        flash('This person is not signed up to play, please try another email address or MAKE THEM SIGN UP!!')
        return render_template("createGame.html")

    # Now it is time to invite the other user by adding it to their invitation list
    invite = GameInvitation(inviter = current_user.id, invitee = user.id)
    db.session.add(invite)
    db.session.commit()

    # then the database will update the sent invitations column for the inviter and the received invites column for the invitee

    return redirect(url_for("web.home"))


@web.route('/test')
def test():
    ter = Territory.query.filter_by(country='Eastern Australia').first()
    return str(ter.neighbours)

@web.route('/populate')
def populate():
    # remove all the territories first
    for ter in Territory.query.all():
        db.session.delete(ter)
    db.session.commit()

    # fakeuser = User(email="fake@gmail.com", name="fake1", password=generate_password_hash("risk12", method='sha256'))
    # db.session.add(fakeuser)
    # fakeuser = User(email="fake2@gmail.com", name="fake2", password=generate_password_hash("risk12", method='sha256'))
    # db.session.add(fakeuser)
    # db.session.commit()

    # create users
    prev_mat = User.query.filter_by(name='mat').first()
    prev_lisa = User.query.filter_by(name='lisa').first()
    if prev_mat is not None:
        db.session.delete(prev_mat)
    if prev_lisa is not None:
        db.session.delete(prev_lisa)
    db.session.commit()
    mat = User(email="bieniekmat@gmail.com", name="mat", password=generate_password_hash("risk12", method='sha256'))
    lis = User(email="pod.features@gmail.com", name="lisa", password=generate_password_hash("risk12", method='sha256'))
    db.session.add(mat)
    db.session.add(lis)
    db.session.commit()

    # create the territories in the database
    for ter, values in territories.items():
        db_ter = Territory(country=ter, locx=values['loc'][0], locy=values['loc'][1])
        db.session.add(db_ter)
    db.session.commit()
    # add the neighbours
    for ter, values in territories.items():
        from_ter = Territory.query.filter_by(country=ter).first()
        for neighbour in values['neighbours']:
            to_ter = Territory.query.filter_by(country=neighbour).first()
            from_ter.neighbours.append(to_ter)
        db.session.add(from_ter)
        db.session.commit()

    return redirect(url_for('auth.login'))


@web.route('/game/<int:gameID>')
@login_required
def getGame(gameID):

    # make sure we know which the correct game is to show

    return render_template('game.html')