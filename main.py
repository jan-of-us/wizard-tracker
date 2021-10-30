import math


def gameplay():

    roundtype = ["Prediction", "Result"]
    # get player count as input, must be 3-6
    pcount = 0
    while int(pcount) < 3 or int(pcount) > 6:
        pcount = input("How many players? ")
    players = int(pcount)
    p_data = []
    for player in range(players):
        data = {}
        data["name"] = input(f"What's Player {player}'s name? ")
        data["points"] = 0
        data["prediction"] = 0
        data["result"] = 0
        p_data.insert(player, data)

    print (p_data)
    # get card count
    cards = 60



    # calculate rounds
    rounds = math.floor(int(cards) / int(players))

    # start gameplay routine
    for round in range(rounds):
        print("Round: " + str(round + 1))
        for type in roundtype:
            for player in p_data:

                inp = input(f"{player['name']}'s {type}: ")







if __name__ == '__main__':
    gameplay()

