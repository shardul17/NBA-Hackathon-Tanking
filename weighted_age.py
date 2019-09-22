import pickle
from pprint import pprint
import numpy as np

#this pickle is a dict of game id: {game date : 2019, team1: {player minutes}, team 2: {player minutes}}
weighted_minutes = pickle.load(open("weighted_minutes.p", "rb"))
game_map = pickle.load(open("game_map.p", "rb"))
#game_map_dates = pickle.load(open("game_map_dates.p", "rb"))

#{player id: dob}
player_dob_hash = pickle.load(open("player_dob_hash.p", 'rb'))

season_minutes = {}
for gameid in weighted_minutes:
    if game_map[gameid] not in season_minutes:
        season_minutes[game_map[gameid]] = {}
    for team in weighted_minutes[gameid]:
        if team == 'Game Date':
            continue
        elif team not in season_minutes[game_map[gameid]]:
            season_minutes[game_map[gameid]][team] = {}
        for player in weighted_minutes[gameid][team]:
            if player not in season_minutes[game_map[gameid]][team]:
                season_minutes[game_map[gameid]][team][player] = weighted_minutes[gameid][team][player]
            else:
                season_minutes[game_map[gameid]][team][player] += weighted_minutes[gameid][team][player]

season_minutes_weighted = {}
for year in season_minutes:
    if year < 2007:
        continue
    elif year not in season_minutes_weighted:
        season_minutes_weighted[year] = {}
    for team in season_minutes[year]:
        total_minutes = sum(season_minutes[year][team].values())
        num_players = len(season_minutes[year][team].keys())
        running_total = 0
        for player in season_minutes[year][team]:
            weight = season_minutes[year][team][player]/total_minutes
#            print(player_dob_hash[player])
            age = year - int(player_dob_hash[player][:4])
            running_total += age*weight
        season_minutes_weighted[year][team] = running_total

"""
weighted_age_difference_bygame = {}
for gameid in weighted_minutes:
    if game_map[gameid] < 2007:
        continue
    weighted_age_difference_bygame[gameid] = {}
    for team in weighted_minutes[gameid]:
        if team == 'Game Date':
            continue
        total_minutes = sum(weighted_minutes[gameid][team].values())
        running_total = 0

        for player in weighted_minutes[gameid][team]:
            weight = weighted_minutes[gameid][team][player]/total_minutes
            age = game_map[gameid] - int(player_dob_hash[player][:4])
            running_total += age*weight
        #season_avg = season_minutes_weighted[game_map[gameid]][team]
        #weighted_age_difference_bygame[gameid][team] = season_avg - running_total
        weighted_age_difference_bygame[gameid][team] = running_total

pprint(weighted_age_difference_bygame)

pickle.dump(weighted_age_difference_bygame, open("weighted_age_difference_bygame.p", "wb"))
"""


#weighted_age_difference_bygame = pickle.load(open("weighted_age_difference_bygame.p", 'rb'))


if __name__ == "__main__":
    #pprint(weighted_age_difference_bygame)
    team_ages_reformat = {}
    for gameid in weighted_age_difference_bygame:
        for team in weighted_age_difference_bygame[gameid]:
            if team not in team_ages_reformat:
                team_ages_reformat[team] = {}
            if game_map[gameid] not in team_ages_reformat[team]:
                team_ages_reformat[team][game_map[gameid]] = []

            team_ages_reformat[team][game_map[gameid]].append((gameid, weighted_age_difference_bygame[gameid][team]))
    for team in team_ages_reformat:
        for year in team_ages_reformat[team]:
            if year != 2011:
                team_ages_reformat[team][year] = team_ages_reformat[team][year][:82]
            else:
                team_ages_reformat[team][year] = team_ages_reformat[team][year][:66]

    for team in team_ages_reformat:
        for year in team_ages_reformat[team]:
            for i in range(len(team_ages_reformat[team][year])):
                #print(team_ages_reformat[team][year][i][1])
                season_avg = season_minutes_weighted[year][team]
                curr_tup = team_ages_reformat[team][year][i]
                new_num = curr_tup[1] - season_avg
                temp_tup = (curr_tup[0], new_num)
                team_ages_reformat[team][year][i] = temp_tup

    pprint(team_ages_reformat)
    #pickle.dump(team_ages_reformat, open("weighted_age_bygame_reformat.p", "wb"))
    #pickle.dump(team_ages_reformat, open("weighted_age_difference_bygame.p", "wb"))


