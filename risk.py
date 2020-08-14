import random


def reinforcements(territories, player_id):
    # Will calculate how many troops a player receives at the beginning of their turn (only based on ters held)
    count = 0
    for ter in territories:
        if ter.owner == player_id:
            count += 1

    if count <= 11:
        return 3
    else:
        reinforcements = count // 3
        return reinforcements


def diceroll(attackerTroops, defenderTroops):
    # simulates a single attack and updates the number of troops accordingly
    # uses the maximum number of troops for attack/defense
    # troop nos are ints

    # checks the attacker has enough men to attack with
    if attackerTroops < 2:
        raise ValueError

    # checks how many dice the attacker gets
    attackerDiceNo = min(attackerTroops, 4) - 1

    # checks how many dice the defender has
    if defenderTroops == 1:
        defenderDiceNo = 1
    else:
        defenderDiceNo = 2

    # simulates diceroll results for attacker and defender
    attackerResults = [random.randint(1, 6) for dice in range(attackerDiceNo)]
    defenderResults = [random.randint(1, 6) for dice in range(defenderDiceNo)]

    # put the results in descending order
    attackerResults.sort(reverse=True)
    defenderResults.sort(reverse=True)

    for attacker_dice, defender_dice in zip(attackerResults, defenderResults):
        # fight!
        if attacker_dice > defender_dice:
            # take one from defender
            defenderTroops -= 1
        else:
            # take one from attacker
            attackerTroops -= 1

    return attackerTroops, defenderTroops


def winGame(game_states, playerID):
    # first calculate no of ters the player has
    count = 0
    for state in game_states:
        if state.owner == playerID:
            count += 1
    if count == 42:
        return True

    return False
