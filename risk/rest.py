import random, time, datetime

from flask_login import current_user
from flask_restful import Resource, Api

from .territories import teralloc, teralloc_db, territories
from .risk_utils import reinforcements, diceroll, winGame
from .db import db
from .models import *


# stages: DEPLOY, REINFORCE, ATTACK, MANOEUVRE, FINAL_MAN, WIN!

def gameModelToDict(game):
    """
    :param game: The database Game object
    :return: A simple dictionary structure that can be converted into json by Flask
    """

    # get all the territories
    risk_territories = {}
    for ter in game.territories:
        country_info = {
            # map info, loc x y, name, neighbours
            'locx': ter.territory.locx,
            'locy': ter.territory.locy,
            'neighbours': [neigh.country for neigh in ter.territory.neighbours],
            # user/game data (who it belongs to etc)
            'troopNo': ter.troopNo,
            'owner': ter.owner,
            # to identify the game state internally
            'id': ter.id
        }
        risk_territories[ter.territory.country] = country_info

    game_dict = {
        'id': game.id,
        'player1': game.player1.id,
        'player2': game.player2.id,
        'currentPlayer': game.currentPlayerId,
        'stage': game.stage,
        'territories': risk_territories,
        'reinNo': game.reinNo,
        'myID': current_user.id,
    }

    return game_dict


def create_game(user1, user2):
    # create a new game
    # decide who goes first
    current_player = random.sample([user1, user2], 1)[0]
    other_player = user1 if current_player == user2 else user2
    # create a game in the database
    game = Game(startDate=datetime.datetime.now(), player1=current_player, player2=other_player, currentPlayerId=current_player.id, stage='DEPLOYMENT')
    db.session.add(game)
    db.session.commit()

    # for each territory, create a gamestate
    game_states = []
    for ter in Territory.query.all():
        game_state = GameState(territoryId=ter.id, territory=ter, game_id=game.id)
        game_states.append(game_state)

    # allocate territories and initial troops to players
    teralloc_db(game_states, [user1, user2])

    # compute the reinforcement number
    game.reinNo = reinforcements(game_states, current_player.id)

    db.session.add(game)
    [db.session.add(gs) for gs in game_states]
    db.session.commit()

    return game


class GetGame(Resource):
    def get(self, gameID):
        # fetch the right game and return it to the user
        game = Game.query.filter_by(id = gameID).first()
        return gameModelToDict(game)


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

        return gameModelToDict(game)


class Diceroll(Resource):
    def put(self, gameID, terFrom, terTo):
        game = Game.query.filter_by(id=gameID).first()

        # TODO check its the right game

        # get the attacking country game state
        country_from = Territory.query.filter_by(country=terFrom).first()
        game_state_from = GameState.query.filter_by(game_id=game.id, territoryId=country_from.id).first()

        # get the defending country game state
        country_to = Territory.query.filter_by(country=terTo).first()
        game_state_to = GameState.query.filter_by(game_id=game.id, territoryId=country_to.id).first()

        # check the troop nos in both countries
        attTroops = game_state_from.troopNo
        defTroops = game_state_to.troopNo

        # perform the attack
        outcomeAtt, outcomeDef = diceroll(attTroops,defTroops)

        # update the countries with the results
        game_state_from.troopNo = outcomeAtt
        game_state_to.troopNo = outcomeDef

        # if the attacker wins the territory then change the owner of the territory and automatically move one troop there
        extra_data = {}
        if (outcomeDef == 0):
            game_state_to.owner = game_state_from.owner
            game_state_to.troopNo = 1
            game_state_from.troopNo -= 1

            # allow the attacker to move in the number of troops of their choice.
            game.stage = "REINFORCE"

            game.reinFrom = game_state_from.id
            game.reinTo = game_state_to.id

        # now update everybody about everything
        db.session.add(game_state_from)
        db.session.add(game_state_to)
        db.session.add(game)
        db.session.commit()

        return gameModelToDict(game)


class Reinforcement(Resource):
    def put(self, gameID, troopNo):

        # check which game it is and TODO check that the person owns it
        game = Game.query.filter_by(id=gameID).first()

        # get the attacking country game state by using game.reinFrom to see where troops will move from
        game_state_from = GameState.query.filter_by(id=game.reinFrom, game_id=game.id).first()

        # get the defending country game state using game.reinTo to see where the troops will move to
        game_state_to = GameState.query.filter_by(id=game.reinTo, game_id=game.id).first()

        # update the troop numbers in the game states
        game_state_from.troopNo -= troopNo
        game_state_to.troopNo += troopNo

        # update the game state
        game.stage = "ATTACK"

        # update the dbs and stuff
        db.session.add(game_state_from)
        db.session.add(game_state_to)
        db.session.add(game)
        db.session.commit()

        return gameModelToDict(game)


class EndMove(Resource):
    def put(self, gameID):
        # check which game it is and TODO check that the person owns it
        game = Game.query.filter_by(id=gameID).first()

        # update the game stage
        game.stage = "MANOEUVRE"

        # update all the things
        db.session.add(game)
        db.session.commit()

        return gameModelToDict(game)


class Man(Resource):
    def put(self, gameID, terFrom, terTo, troopNo):

        # check which game it is and TODO check that the person owns it
        game = Game.query.filter_by(id=gameID).first()

        # move the final manoeuvred troops from the old to the new place
        # get the attacking country game state and remove the troops
        country_from = Territory.query.filter_by(country=terFrom).first()
        game_state_from = GameState.query.filter_by(game_id=game.id, territoryId=country_from.id).first()
        game_state_from.troopNo -= troopNo

        # get the defending country game state and add the troops
        country_to = Territory.query.filter_by(country=terTo).first()
        game_state_to = GameState.query.filter_by(game_id=game.id, territoryId=country_to.id).first()
        game_state_to.troopNo += troopNo

        # change the player so it's the next players turn
        if game.currentPlayerId == game.player1:
            game.currentPlayerId = game.player2
        else:
            game.currentPlayerId = game.player1

        # update the game stage
        game.stage = "DEPLOYMENT"

        # calculate the no of troops the next player can deploy at the beginning of their turn
        all_game_states = GameState.query.filter_by(game_id=game.id).all()
        game.reinNo = reinforcements(all_game_states, game.currentPlayerId)

        # update the dbs and stuff
        db.session.add(game_state_from)
        db.session.add(game_state_to)
        db.session.add(game)
        db.session.commit()

        return gameModelToDict(game)


class EndTurn(Resource):
    def put(self, gameID):
        game = Game.query.filter_by(id=gameID).first()
        all_game_states = GameState.query.filter_by(game_id=game.id).all()

        if winGame(all_game_states, game.currentPlayerId):
            game.stage = 'WIN!'
            db.session.add(game)
            db.session.commit()
            return gameModelToDict(game)
        else:
            if game.currentPlayerId == game.player1.id:
                game.currentPlayerId = game.player2.id
            else:
                game.currentPlayerId = game.player1.id

            game.stage = "DEPLOYMENT"
            game.reinNo = reinforcements(all_game_states, game.currentPlayerId)
            db.session.add(game)
            db.session.commit()

            return gameModelToDict(game)



class Reject(Resource):
    def put(self, email):
        # check which game it is and TODO check that the person owns it
        inviter_user = User.query.filter_by(email=email).first()
        if not inviter_user:
            raise NotImplementedError('do me')

        game_invite = GameInvitation.query.filter_by(inviter=inviter_user.id, invitee=current_user.id).first()

        # update all the things
        db.session.delete(game_invite)
        db.session.commit()

        return {'email': inviter_user.email}


class Accept(Resource):
    def put(self, email):

        # check which game it is and TODO check that the person owns it
        inviter_user = User.query.filter_by(email=email).first()
        if not inviter_user:
            raise NotImplementedError('do me')

        # find the game invite so we can delete that from the database GameInvitations table
        game_invite = GameInvitation.query.filter_by(inviter=inviter_user.id, invitee=current_user.id).first()

        # create the new game (which can then be put into the ongoing games column)
        # note: new game commited in the new game function
        game = create_game(inviter_user, current_user)

        # update all the things
        db.session.delete(game_invite)
        db.session.commit()

        return {'email': inviter_user.email, 'game_id': game.id}


class Refresh(Resource):
    def get(self, gameID):
        # get the correct game
        game = Game.query.filter_by(id=gameID).first()

        # loops 19 times so it will time out in roughly a minute
        for i in range(19):
            # refreshes the db query to check if the game is ready to be refreshed
            # see (https://www.michaelcho.me/article/sqlalchemy-commit-flush-expire-refresh-merge-whats-the-difference)
            db.session.refresh(game)

            # if it has returned to the current users turn then it refreshes the game
            if current_user.id == game.currentPlayerId:
                return gameModelToDict(game)

            # otherwise makes it sleep so it's not checking too many times
            time.sleep(3)

        # make sure the query is up to date
        db.session.refresh(game)
        return gameModelToDict(game)


def register_rest_api(app):
    api = Api(app)

    # meta
    api.add_resource(Reject, '/REST/reject/<string:email>')
    api.add_resource(Accept, '/REST/accept/<string:email>')

    api.add_resource(GetGame, '/REST/game/<int:gameID>')
    api.add_resource(Deployment, '/REST/deployment/<int:gameID>/<string:country>')
    api.add_resource(Diceroll, '/REST/diceroll/<int:gameID>/<string:terFrom>/<string:terTo>')
    api.add_resource(Reinforcement, '/REST/reinforcement/<int:gameID>/<int:troopNo>')
    api.add_resource(EndMove, '/REST/endmove/<int:gameID>')
    api.add_resource(Man, '/REST/man/<int:gameID>/<string:terFrom>/<string:terTo>/<int:troopNo>')
    api.add_resource(EndTurn, '/REST/endTurn/<int:gameID>')
    api.add_resource(Refresh, '/REST/refresh/<int:gameID>')
