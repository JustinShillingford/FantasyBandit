import math
import random
import csv
import numpy as np


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

# Inputs:
# [start_year] is the year to begin retrieving player data from
# [check_year] is the year to retrieve player data from to compare team roster with algorithm results
# [team] is the NBA team to retrieve player data from
#
# Returns an array where:
# - the first element is a list of all players of a given [team] from the [start_year] to two years later
# - the second element is the list of players on the given [team] the year following the algorithm's analysis


def initPlayersList():
    with open('nba-players-stats/2021Stats.csv') as statsCSV:
        reader = csv.reader(statsCSV, delimiter=',')
        firstLine = True
        players = []

        # create dictionaries to keep track of players across multiple records
        player_seen_dict = {}
        player_index_dict = {}

        # create list to compare algorithm results with
        check_players = []

        for row in reader:
            if (firstLine):
                firstLine = False
            else:
                # Player Processing Code goes here

                # Name = row[2]
                # PER = row[9]
                # +/- = row[29]
                # Win Shares = row[24]
                # Games Played = row[6]

                # only include players within specified team and year range
                name = row[1]
                per = row[7]
                winShares = row[22]
                gamesPlayed = row[5]

                if name in player_seen_dict:
                    # increment num_times_seen
                    player_seen_dict[name] += 1

                    # increment player values
                    players[player_index_dict[name]
                            ].rewardSum += float(per)
                    players[player_index_dict[name]].per += float(per)
                    players[player_index_dict[name]
                            ].winShares += float(winShares)
                    players[player_index_dict[name]
                            ].gamesPlayed += float(gamesPlayed)
                    players[player_index_dict[name]
                            ].probability += players[player_index_dict[name]].gamesPlayed

                else:
                    # add player to dictionary
                    player_seen_dict[name] = 1
                    # next index is length of list
                    player_index_dict[name] = len(players)

                    # 0's are used as placeholders for the calculated values
                    players.append(Player(name, float(per), 0, 0, float(
                        gamesPlayed), float(per), float(winShares), float(gamesPlayed)))

        # average each player's values
        for i in range(0, len(players)):
            num_times_seen = player_seen_dict[players[i].name]

            players[i].rewardSum /= num_times_seen
            players[i].per /= num_times_seen
            players[i].winShares /= num_times_seen
            players[i].gamesPlayed /= num_times_seen
            players[i].probability /= (82 * num_times_seen)

    return [players, check_players]


def exploration(player, totalPulls):
    return (2 * math.sqrt(math.log(totalPulls))) / (math.sqrt(player.numPulls))


def exploitation(player):
    return (player.rewardSum) / (player.numPulls)


def reward(player):
    if (random.random() > player.probability):
        return 0
    else:
        return player.gamesPlayed * player.per

# Returns a list of marks that coincide with the indicies of the [players] list that
# indicates whether to keep a player (1) or remove the player (0) from the team.


def multiArmedBandit(players):
    exploreVsExploit_lst = []
    keep = []
    kept = 0

    for i in range(len(players)):
        players[i].rewardSum = reward(players[i])
        players[i].numPulls = 1
        players[i].exploreVsExploit = 0

        exploreVsExploit_lst.append(0)
        keep.append(0)

    # At this point, you've pulled everything once
    totalPulls = len(players)

    while(kept < 180):
        # Pick argmax from exploreVsExploit, then look at that corresponding player in players array
        bestPlayerIndex = np.argmax(exploreVsExploit_lst)

        # Add a pull for the best player, update rewardSum for player that's been pulled
        players[bestPlayerIndex].numPulls += 1
        players[bestPlayerIndex].rewardSum += reward(players[bestPlayerIndex])

        # Prep for next pull
        totalPulls += 1
        # Go thru and update exploreVsExploit for ALL players on next (N+1) pull
        for i in range(len(players)):
            if keep[i] != 1:    # player hasn't been chosen to stay
                exploreVsExploit_lst[i] = exploration(
                    players[i], totalPulls) + exploitation(players[i])
            else:               # stop updating kept player
                exploreVsExploit_lst[i] = 0

        # Mark a player if we choose to keep them
        if(players[bestPlayerIndex].numPulls > 50):
            keep[bestPlayerIndex] = 1               # mark the player
            kept += 1
            # prevent player from being selected again
            exploreVsExploit_lst[bestPlayerIndex] = 0

    return keep

# Inputs:
# [keep] is the list of marks that indicate whether a player was selected to stay on the team
# [following_yr_lst] is the list of player names that are on the team the year following the algorithm's analysis
# [all] is the list of all Player objects that have been on the specified team during the given years
#
# Returns an array where:
# - the first element is the suggested number of players to be removed
# - the second element is the number of players that remained on the team despite suggesting otherwise


def print_players(keep, following_yr_lst, all):
    # lists to store player names
    players_kept = []
    players_removed = []
    failure_count = 0

    sortedList = sorted(all, key=lambda x: x.rewardSum, reverse=True)

    # create lists and concurrently print kept players
    for i in range(0, len(sortedList)):
        if keep[i] == 1:
            players_kept.append(sortedList[i].name)
            print("Keep: " + sortedList[i].name +
                  " " + str(sortedList[i].rewardSum))
        else:
            players_removed.append(sortedList[i].name)
            if sortedList[i].name in following_yr_lst:
                failure_count += 1
    print("-----------------------------------")
    # print removed players
    for i in range(0, len(players_removed)):
        print("Remove: " + players_removed[i])

    return [len(players_removed), failure_count]


# [team] is a string version of the acronym for a given team
# [start_year] is the year to begin running the algorithm on
#
# Note: When [start_year] > 2015, [start_year] is defaulted to 2015 to allow the
# algorithm to run across 3 years.
# When [start_year] = 2015, [check_year] will be defaulted to 2017 to fetch the most
# recent player data available for evaluation. However, since 2017 is included in the
# algorithm's analysis, the success rate will be lower.
def runBandit():
    players = initPlayersList()
    np_players = np.array(players[0])
    kept_player_indices = multiArmedBandit(np_players)

    check_info = print_players(kept_player_indices, players[1], np_players)


runBandit()
