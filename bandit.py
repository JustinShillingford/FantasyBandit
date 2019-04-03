import math
import random
import numpy

def multiArmedBandit(self, players):
    for player as players:
        player["rewardSum"] = self.reward(player)
        player["numPulls"] = 1
        player["exploreVsExploit"] = 0

    totalPulls = len(players)

    while(True):
        bestPlayer = None

        for player as players:
            if ((self.exploitation(player) + self.exploration(player, totalPulls)) > bestPlayer["exploreVsExploit"]):
                player["exploreVsExploit"] = self.exploitation(player) + self.exploration(player, totalPulls)
                bestPlayer = player

        bestPlayer["rewardSum"] += self.reward(bestPlayer)
        bestPlayer["numPulls"] += 1
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

