import random

from flask_login import current_user
from flask_restful import Resource, Api

from territories import teralloc, teralloc_db, territories
from risk import reinforcements_db, diceroll, winGame
from db import db
from models import *


# stages: DEPLOY, REINFORCE, ATTACK, MANOEUVRE, FINAL_MAN, WIN!

def create_game(user1, user2):
    # A NEW GAME
    # create a new game
    # decide who goes first
    current_player = random.sample([user1, user1], 1)[0]
    other_player = user1 if current_player == user2 else user2
    # create a game in the database
    game = Game(player1=current_player, player2=other_player, currentPlayer=current_player.id, stage='DEPLOYMENT')
    db.session.add(game)
    db.session.commit()

    # for each territory, create a gamestate
    game_states = []
    for ter in Territory.query.all():
        game_state = GameState(territoryId=ter.id, game_id=game.id)
        game_states.append(game_state)

    # allocate territories and initial troops to players
    teralloc_db(game_states, [user1, user2])

    # compute the reinforcement number
    game.reinNo = reinforcements_db(game_states, current_player.id)

    db.session.add(game)
    [db.session.add(gs) for gs in game_states]
    db.session.commit()

    return game

class TroopResource(Resource):
    """
        1. Allocate territories
        2. Set the stage to reinforcment
    """
    def get(self):
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
        game.reinNo = reinforcements_db(game_states, current_player.id)

        db.session.add(game)
        [db.session.add(gs) for gs in game_states]
        db.session.commit()

        return game.get_risk_json()


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

        return game.get_risk_json()


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

        return game.get_risk_json()


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

        return game.get_risk_json()


class EndMove(Resource):
    def put(self, gameID):
        # check which game it is and TODO check that the person owns it
        game = Game.query.filter_by(id=gameID).first()

        # update the game stage
        game.stage = "MANOEUVRE"

        # update all the things
        db.session.add(game)
        db.session.commit()

        return game.get_risk_json()


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
        if game.currentPlayer == 1:
            game.currentPlayer = 2
        else:
            game.currentPlayer = 1

        # update the game stage
        game.stage = "DEPLOYMENT"

        # calculate the no of troops the next player can deploy at the beginning of their turn
        all_game_states = GameState.query.filter_by(game_id=game.id).all()
        game.reinNo = reinforcements_db(all_game_states, game.currentPlayer)

        # update the dbs and stuff
        db.session.add(game_state_from)
        db.session.add(game_state_to)
        db.session.add(game)
        db.session.commit()

        return game.get_risk_json()


class EndTurn(Resource):
    def put(self, gameID):
        game = Game.query.filter_by(id=gameID).first()
        all_game_states = GameState.query.filter_by(game_id=game.id).all()

        if winGame(all_game_states, game.currentPlayer):
            game.stage = 'WIN!'
            db.session.add(game)
            db.session.commit()
            return game.get_risk_json()
        else:
            if game.currentPlayer == 1:
                game.currentPlayer = 2
            else:
                game.currentPlayer = 1

            game.stage = "DEPLOYMENT"
            game.reinNo = reinforcements_db(all_game_states, game.currentPlayer)
            db.session.add(game)
            db.session.commit()

            return game.get_risk_json()



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
        game = create_game(inviter_user, current_user)

        # update all the things
        db.session.delete(game_invite)
        db.session.commit()

        return {'email': inviter_user.email, 'game_id': game.id}



def register_rest_api(app):
    api = Api(app)

    # meta
    api.add_resource(Reject, '/REST/reject/<string:email>')
    api.add_resource(Accept, '/REST/accept/<string:email>')

    api.add_resource(TroopResource, '/REST/countries')
    api.add_resource(Deployment, '/REST/deployment/<int:gameID>/<string:country>')
    api.add_resource(Diceroll, '/REST/diceroll/<int:gameID>/<string:terFrom>/<string:terTo>')
    api.add_resource(Reinforcement, '/REST/reinforcement/<int:gameID>/<int:troopNo>')
    api.add_resource(EndMove, '/REST/endmove/<int:gameID>')
    api.add_resource(Man, '/REST/man/<int:gameID>/<string:terFrom>/<string:terTo>/<int:troopNo>')
    api.add_resource(EndTurn, '/REST/endTurn/<int:gameID>')