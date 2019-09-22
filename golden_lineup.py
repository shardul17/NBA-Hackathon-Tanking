import gzip
import pandas as pd
import pickle
import operator
from itertools import permutations
from itertools import combinations
from pprint import pprint
import numpy as np


def getStringYear(year):
    string_year = ''
    if year in [2007,2008]:
        string_year = str(year) + "-0" + str(int(str(year)[-1]) + 1)
    elif year == 2009:
        string_year = '2009-10'
    else:
        string_year = str(year) + "-" + str(int(str(year)[-2:]) + 1)
    return string_year

def getFiveManLineups(game_active_players):
    list_of_sets = []
    temp_ting = list(combinations(game_active_players,5))
    for combo in range(len(temp_ting)):
        temp_set = set()
        for name in range(len(temp_ting[combo])):
            ind_name_list = temp_ting[combo][name].split(' ')
            if len(ind_name_list) == 1:
                str = '.' + ind_name_list[0]
                temp_set.add(str)
            elif len(ind_name_list) == 2:
                str = '.' + ind_name_list[0][0] + '. ' + ind_name_list[1]
                temp_set.add(str)
            elif len(ind_name_list) == 3:
                str = '.' + ind_name_list[0][0] + '. ' + ind_name_list[1] + ' ' + ind_name_list[2]
                temp_set.add(str)
        list_of_sets.append(temp_set)
    return list_of_sets

def getNetRtgList(temp_lineups):
    netrtgList = []
    for lineup in temp_lineups:
        lineup_list = lineup.split(', ')
        lineup_list[4] = lineup_list[4][:-1]
        temp_set = set()
        for name in lineup_list:
            temp_set.add(name)
        netrtg = float(temp_lineups[lineup]['NETRTG'])
        minutes = float(temp_lineups[lineup]['MIN'])
        netrtgList.append((temp_set, netrtg, minutes))
    netrtgList = sorted(netrtgList,key=lambda x: x[1], reverse=True)
    return netrtgList

def getGoldenLineup(netRatings, rotationCombos):
    golden_lineup = set()

    for tup in range(len(netRatings)):
        if netRatings[tup][0] in rotationCombos:
            golden_lineup = netRatings[tup][0]
            break

    return golden_lineup


if __name__ == "__main__":

    lineup_data = pickle.load(open("lineup_data.p", "rb"))
    active_players = pickle.load(open("active_lineups.p", "rb"))

    golden_lineup = {}

    for year in active_players:
        print(year)
        string_year = getStringYear(year)
        for game in active_players[year]:
            #print(golden_lineup)
            for team in active_players[year][game]:
                temp_lineups = lineup_data[string_year][team]
                # this is a list: [(first_elem is a lineup set, second is the lineups net ratings, third is MPG)..]
                netrtgList = getNetRtgList(temp_lineups)
                curr_active_players = active_players[year][game][team]

                # filter based on MPG
                netrtgList.sort(key=lambda x: x[2], reverse = True)
                MPG = np.array([i[2] for i in netrtgList])
                mean_minutes = MPG.mean()
                std_minutes = MPG.std()

                filtered_lineup = list(filter(lambda x: x[2] > (mean_minutes + 1*std_minutes), netrtgList))
                filtered_lineup.sort(key = lambda x: x[1], reverse = True)

                temp_set = set()
                for name in active_players[year][game][team]:
                    ind_name_list = name.split(' ')
                    if len(ind_name_list) == 1:
                        string = '.' + ind_name_list[0]
                        temp_set.add(string)
                    elif len(ind_name_list) == 2:
                        string = '.' + ind_name_list[0][0] + '. ' + ind_name_list[1]
                        temp_set.add(string)
                    elif len(ind_name_list) == 3:
                        string = '.' + ind_name_list[0][0] + '. ' + ind_name_list[1] + ' ' + ind_name_list[2]
                        temp_set.add(string)

                best = None
                best_num_features = float('-inf')
                for lineup, rating, minutes in filtered_lineup:
                    intersect = lineup.intersection(temp_set)
                    if len(intersect) == 5:
                        best = lineup
                        break
                    elif len(intersect) > best_num_features:
                        best = lineup
                        best_num_features = len(intersect)

                if game not in golden_lineup:
                    golden_lineup[game] = {}
                    golden_lineup[game][team] = best
                else:
                    golden_lineup[game][team] = best

    pickle.dump(golden_lineup, open("golden_lineup.p", "wb"))
    pprint(golden_lineup)