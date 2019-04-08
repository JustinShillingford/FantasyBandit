import math
import random
import csv

class Player:
    """
        The class that sets up a Player and their relevant attributes
    """
    def __init__(self, name, rewardSum, numPulls, exploreVsExploit, probability, per, winShares, gamesPlayed):
        self.name = name
        self.rewardSum = rewardSum
        self.numPulls = numPulls
        self.exploreVsExploit = exploreVsExploit
        self.probability = probability

        self.per = per
        self.winShares = winShares
        self.gamesPlayed = gamesPlayed

def initPlayersList():
    with open('nba-players-stats/Seasons_Stats.csv') as statsCSV:
        reader = csv.reader(statsCSV, delimiter=',')
        firstLine = True
        players = []
        last_player = ""
        for row in reader:
            if (firstLine):
                firstLine = False
            else:
                # Player Processing Code goes here

                # Name = row[2]
                # PER = row[9]
                # Win Shares = row[24]
                # Games Played = row[6] <-- The numbers on this one look kinda weird for some reason

                # check if there are multiple rows of identical player
                # first row a player appears in always tends to be TOT, so we only need to store that one
                if last_player != row[2]:
                    name = row[2]
                    per = row[9]
                    winShares = row[24]
                    gamesPlayed = row[6]

                    # 0's are used as placeholders for the calculated values
                    players.append(Player(name, 0, 0, 0, 0, per, winShares, gamesPlayed))
                    
                    last_player = name
    return players

def exploration(player, totalPulls):
    return (2 * math.sqrt(math.log(totalPulls))) / (math.sqrt(player.numPulls))

def exploitation(player):
    return (player.rewardSum) / (player.numPulls)

def reward(player):
    if (random.random() > player.probability):
        return 0
    else:
        return player.rewardSum

def multiArmedBandit(players):
    for player in players:
        player.rewardSum = reward(player)
        player.numPulls = 1
        player.exploreVsExploit = 0

    totalPulls = len(players)

    while(True):
        bestPlayerIndex = 0

        # Loop to calculate argmax
        for i in range(len(players)):
            if ((exploitation(players[i]) + exploration(players[i], totalPulls)) > players[bestPlayerIndex].exploreVsExploit):
                players[i].exploreVsExploit = exploitation(players[i]) + exploration(players[i], totalPulls)
                bestPlayerIndex = i

        players[bestPlayerIndex].rewardSum += reward(players[bestPlayerIndex])
        players[bestPlayerIndex].numPulls += 1
        totalPulls += 1
        print("Selected: " + players[bestPlayerIndex].name + ". I've selected them " + str(players[bestPlayerIndex].numPulls) + " times.")


players = initPlayersList()
multiArmedBandit(players)