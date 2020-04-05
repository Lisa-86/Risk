import random


# p1troops = 10
# p2troops = 5

def diceroll(p1troops, p2troops):
    player_1 = []
    player_2 = []

    if p1troops < 1:
        raise ValueError
    if p1troops == 1:
        p1dice = 1
    if p1troops == 2:
        p1dice = 2
    if p1troops > 2:
        p1dice = 3

    if p2troops == 1:
        p2dice = 1
    if p2troops > 1:
        p2dice = 2

    for dice in range(p1dice):
        randomno = int(random.uniform(1, 6))
        player_1.append(randomno)

    for dice in range(p2dice):
        randomno = int(random.uniform(1, 6))
        player_2.append(randomno)

    player_1.sort(reverse=True)
    player_2.sort(reverse=True)

    print("player 1", player_1)
    print("player 2", player_2)

    if len(player_1) < len(player_2):
        shorterlist = player_1

    else:
        shorterlist = player_2

    print("the shorter list is", shorterlist)

    if len(shorterlist) == 1:

        if player_1[0] > player_2[0]:
            p2troops -= 1
            print("player 2 loses a troop, now has", p2troops)
        else:
            p1troops -= 1
            print("player 1 loses a troop, now has", p1troops)

        if p2troops == 0:
            print("player 1 has won this territory from player 2")

        return p1troops, p2troops

    if len(shorterlist) == 2:

        if player_1[0] > player_2[0]:
            p2troops -= 1
            print("player 2 loses a troop, now has", p2troops)

        if player_1[0] <= player_2[0]:
            p1troops -= 1
            print("player 1 loses a troop, now has", p1troops)

        if player_1[1] > player_2[1]:
            p2troops -= 1
            print("player 2 loses a troop, now has", p2troops)

        if player_1[1] <= player_2[1]:
            p1troops -= 1
            print("player 1 loses a troop, now has", p1troops)

        if p2troops == 0:
            print("player 1 has won this territory from player 2")

        return p1troops, p2troops


p1troops, p2troops = diceroll(1, 4)
if p1troops == 0:
    print("not enough troops to attack")

print("p1troops:", p1troops)
print("p2troops:", p2troops)



