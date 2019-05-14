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
def initPlayersList(start_year, check_year, team):
    with open('nba-players-stats/Seasons_Stats.csv') as statsCSV:
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
            elif team != None:
                # Player Processing Code goes here

                # Name = row[2]
                # PER = row[9]
                # +/- = row[29]
                # Win Shares = row[24]
                # Games Played = row[6] <-- The numbers on this one look kinda weird for some reason

                # only include players within specified team and year range
                if team == row[5].lower() and len(row[2]) > 0 and len(row[9]) > 0 and int(row[1]) >= start_year and (int(row[1]) <= start_year + 2):
                    name = row[2]
                    per = row[9]
                    winShares = row[24]
                    gamesPlayed = row[6]
                    year = row[1]

                    if name in player_seen_dict:
                        player_seen_dict[name] += 1     # increment num_times_seen

                        # increment player values
                        players[player_index_dict[name]].rewardSum += float(per)
                        players[player_index_dict[name]].per += float(per)
                        players[player_index_dict[name]].winShares += float(winShares)
                        players[player_index_dict[name]].gamesPlayed += float(gamesPlayed)
                        players[player_index_dict[name]].probability += players[player_index_dict[name]].gamesPlayed

                    else:
                        player_seen_dict[name] = 1      # add player to dictionary
                        player_index_dict[name] = len(players)  # next index is length of list

                        # 0's are used as placeholders for the calculated values
                        players.append(Player(name, float(per), 0, 0, float(gamesPlayed), float(per), float(winShares), float(gamesPlayed)))
                
                # get list of player names who are still on the team the following year
                if team == row[5].lower() and len(row[2]) > 0 and len(row[9]) > 0 and int(row[1]) == check_year:
                    check_players.append(row[2])

        # average each player's values
        for i in range (0, len(players)):
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
        return float(player.per)

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

    while(kept < 15):

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
                exploreVsExploit_lst[i] = exploration(players[i], totalPulls) + exploitation(players[i])
            else:               # stop updating kept player
                exploreVsExploit_lst[i] = 0

        # Mark a player if we choose to keep them
        if(players[bestPlayerIndex].numPulls > 50):
            keep[bestPlayerIndex] = 1               # mark the player
            kept += 1
            exploreVsExploit_lst[bestPlayerIndex] = 0   # prevent player from being selected again

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

    # create lists and concurrently print kept players
    for i in range(0, len(all)):
        if keep[i] == 1:
            players_kept.append(all[i].name)
            print("Keep: " + all[i].name)
        else:
            players_removed.append(all[i].name)
            if all[i].name in following_yr_lst:
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
def runBandit(start_year, team):
    check_year = (start_year + 3 <= 2017) and (start_year + 3) or 2017  # selected year to form eval on results

    players = initPlayersList(start_year, check_year, team)
    np_players = np.array(players[0])
    kept_player_indices = multiArmedBandit(np_players)

    check_info = print_players(kept_player_indices, players[1], np_players)

    num_successes = check_info[0] - check_info[1]
    print(str(num_successes) + " out of " + str(check_info[0]) + " suggested players to be removed were no longer on the team in " + str(check_year))



# only works in python 2.7, later versions require 'input' function
team = raw_input("Enter the official acronym for the team you're interested in or 'None' otherwise: ").lower()

start_year = int(raw_input("Player data is available for 2000-2017. Algorithm will use 3 consecutive years inclusive. Enter a specific year to begin retrieving data from: "))
start_year = (start_year > 2015) and 2015 or start_year

if team != "none":
    runBandit(start_year, team)
else:
    runBandit(start_year)