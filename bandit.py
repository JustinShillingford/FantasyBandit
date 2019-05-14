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

# make a dictionary of player names
    # key = player name, value = number of times seen
# if in dictionary, just increment all the values & num_times_seen
# else, create the values and add to dictionary

# at the end, average values out

def initPlayersList(start_year, team):
    with open('nba-players-stats/Seasons_Stats.csv') as statsCSV:
        reader = csv.reader(statsCSV, delimiter=',')
        firstLine = True
        players = []
        player_seen_dict = {}
        player_index_dict = {}
        last_player = ""
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

                # only include players within specified team
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

                        #if int(year) >= 2000:
                            # 0's are used as placeholders for the calculated values
                        players.append(Player(name, float(per), 0, 0, (float(gamesPlayed) / 82), float(per), float(winShares), float(gamesPlayed)))
                            #players.append(Player(name, float(per), 0, 0, (float(gamesPlayed) / 82), per, winShares, gamesPlayed))

            else:
                # check if there are multiple rows of identical player
                # first row a player appears in always tends to be TOT, so we only need to store that one
                if last_player != row[2]:
                    name = row[2]
                    per = row[9]
                    winShares = row[24]
                    gamesPlayed = row[6]
                    year = row[1]

                    if len(name) > 0 and int(year) >= 2000 and len(per) > 0:
                        # 0's are used as placeholders for the calculated values
                        players.append(Player(name, float(per), 0, 0, (float(gamesPlayed) / 82), per, winShares, gamesPlayed))

                    last_player = name

        # average each player's values
        for i in range (0, len(players)):
            num_times_seen = player_seen_dict[players[i].name]

            players[i].rewardSum /= num_times_seen
            players[i].per /= num_times_seen
            players[i].winShares /= num_times_seen
            players[i].gamesPlayed /= num_times_seen
            players[i].probability /= (82 * num_times_seen)

    print("Length of players = " + str(len(players)))
    return players

def exploration(player, totalPulls):
    return (2 * math.sqrt(math.log(totalPulls))) / (math.sqrt(player.numPulls))

def exploitation(player):
    return (player.rewardSum) / (player.numPulls)

def reward(player):
    if (random.random() > player.probability):
        return 0
    else:
        return float(player.per)

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
        #print("index = " + str(bestPlayerIndex) + " - ")

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

        # print(exploreVsExploit_lst)

        # Mark a player if we choose to keep
        if(players[bestPlayerIndex].numPulls > 50):
            keep[bestPlayerIndex] = 1               # mark the player
            kept += 1
            exploreVsExploit_lst[bestPlayerIndex] = 0   # prevent player from being selected again

        #print("Selected: " + players[bestPlayerIndex].name + ". I've selected them " + str(players[bestPlayerIndex].numPulls) + " times.")

    return keep

def print_players(keep, all):
    # lists to store player names
    players_kept = []
    players_removed = []

    # create lists and concurrently print kept players
    for i in range(0, len(all)):
        if keep[i] == 1:
            players_kept.append(all[i].name)
            print("Keep: " + all[i].name)
        else:
            players_removed.append(all[i].name)

    # print removed players
    # for i in range(0, len(players_removed)):
    #     print("Remove: " + players_removed[i])

# team is a string version of the acronym for a given team
def runBandit(start_year, team = None):
    players = initPlayersList(start_year, team)
    np_players = np.array(players)
    kept_player_indices = multiArmedBandit(np_players)
    print_players(kept_player_indices, np_players)

# only works in python 2.7, later versions require 'input' function
team = raw_input("Enter the official acronym for the team you're interested in or 'None' otherwise: ").lower()
#select_year = raw_input("Player data is obtained from 2000-2017 by default. Would you like to specify a year range? Enter 'Y' for yes or 'N' for no.").lower()
start_year = int(raw_input("Player data is available for 2000-2017. Algorithm will use 3 consecutive years inclusive. Enter a specific year to begin retrieving data from: "))

start_year = (start_year > 2015) and 2015 or start_year
# if (select_year == "y"):
#     start_year = int(raw_input("Enter a start year in the range [2000, 2017]: "))
#     end_year = int(raw_input("Enter an end year in the range [2000, 2017]: "))

if team != "none":
    runBandit(start_year, team)
else:
    runBandit(start_year)

# give user year selection
# average each player's data for all years
# give precedence to recent performance somehow