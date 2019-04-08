import math
import random
import csv

class Player:
    """
        The class that sets up a Player and their relevant attributes
    """
    def __init__(self, name, rewardSum, numPulls, exploreVsExploit, probability):
        self.name = name
        self.rewardSum = rewardSum
        self.numPulls = numPulls
        self.exploreVsExploit = exploreVsExploit
        self.probability = probability

def initPlayersList(self):
    with open('nba-players-stats/Seasons_Stats.csv') as statsCSV:
        reader = csv.reader(statsCSV, delimiter=',')
        firstLine = True
        for row in reader:
            if (firstLine):
                firstLine = False
            else:
                # Player Processing Code goes here

                # Name = row[2]
                # PER = row[9]
                # Win Shares = row[24]
                # Games Played = row[6] <-- The numbers on this one look kinda weird for some reason


def multiArmedBandit(self, players):
    for player as players:
        player["rewardSum"] = self.reward(player)
        player["numPulls"] = 1
        player["exploreVsExploit"] = 0

    totalPulls = len(players)

    while(True):
        bestPlayerIndex = None

        # Loop to calculate argmax
        for i in range(len(players)):
            if ((self.exploitation(players[i]) + self.exploration(players[i], totalPulls)) > players[bestPlayerIndex]["exploreVsExploit"]):
                players[i]["exploreVsExploit"] = self.exploitation(players[i]) + self.exploration(players[i], totalPulls)
                bestPlayerIndex = i

        players[bestPlayerIndex]["rewardSum"] += self.reward(players[bestPlayerIndex])
        players[bestPlayerIndex]["numPulls"] += 1
        totalPulls += 1
        print("Selected: " + players[bestPlayerIndex]["name"] + ". I've selected them " + players[bestPlayerIndex]["numPulls"] + " times.")

def exploration(self, player, totalPulls):
    return (2 * math.sqrt(math.log(totalPulls))) / (math.sqrt(player["numPulls"]))

def exploitation(self, player):
    return (player["rewardSum"]) / (player["numPulls"])

def reward(self, player):
    if (random.random() > player["probability"]):
        return 0
    else:
        return player["rewardSum"]

