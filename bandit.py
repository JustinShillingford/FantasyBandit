import math
import random

def multiArmedBandit(self, players):
    for player as players:
        player["rewardSum"] = self.reward(player)
        player["numPulls"] = 1
        player["exploreVsExploit"] = 0

    totalPulls = len(players)

    while(True):
        bestPlayerIndex = None

        for i in range(len(players)):
            if ((self.exploitation(players[i]) + self.exploration(players[i], totalPulls)) > players[bestPlayerIndex]["exploreVsExploit"]):
                players[i]["exploreVsExploit"] = self.exploitation(players[i]) + self.exploration(players[i], totalPulls)
                bestPlayerIndex = i

        players[bestPlayerIndex]["rewardSum"] += self.reward(players[bestPlayerIndex])
        players[bestPlayerIndex]["numPulls"] += 1
        totalPulls += 1

def exploration(self, player, totalPulls):
    return (2 * math.sqrt(math.log(totalPulls))) / (math.sqrt(player["numPulls"]))

def exploitation(self, player):
    return (player["rewardSum"]) / (player["numPulls"])

def reward(self, player):
    if (random.random() > player["probability"]):
        return 0
    else:
        return player["rewardSum"]

