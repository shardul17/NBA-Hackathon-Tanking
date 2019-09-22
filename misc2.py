import pickle
from pprint import pprint
import matplotlib.pyplot as plt
import statistics as stat
import numpy as np
from selenium import webdriver
from pandas import *
import pandas
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import *
import requests
from lxml import html

player_dob_hash = pickle.load(open("player_dob_hash.p", "rb"))
golden_minutes_reformat = pickle.load(open("golden_minutes_reformat.p", 'rb'))
weighted_age_bygame_reformat = pickle.load(open("weighted_age_bygame_reformat.p", 'rb'))
team_map = pickle.load(open("team_mapping.p", 'rb'))
off_def_rating = pickle.load(open("off_def_rating.p", 'rb'))


pace = pickle.load(open("pace.p", 'rb'))
pie = pickle.load(open("pie.p", 'rb'))
temp_off = pickle.load(open("off_rating.p", 'rb'))
temp_def = pickle.load(open("def_rating.p", 'rb'))

for team in pace:
    for year in pace[team]:
        numbers = [float(x) for x in pace[team][year]]
        pace[team][year] = numbers
        pace_mean = sum(pace[team][year])/len(pace[team][year])

        numbers = [float(x) for x in pie[team][year]]
        pie[team][year] = numbers
        pie_mean = sum(pie[team][year])/len(pie[team][year])

        numbers = [float(x) for x in temp_off[team][year]]
        temp_off[team][year] = numbers
        off_mean = sum(temp_off[team][year])/len(temp_off[team][year])

        numbers = [float(x) for x in temp_def[team][year]]
        temp_def[team][year] = numbers
        def_mean = sum(temp_def[team][year])/len(temp_def[team][year])

        paceman = list(map(lambda x: x-pace_mean, pace[team][year]))
        pieman = list(map(lambda x: x-pie_mean, pie[team][year]))
        offman = list(map(lambda x: x-off_mean, temp_off[team][year]))
        defman = list(map(lambda x: x-def_mean, temp_def[team][year]))

        pace[team][year] = paceman
        pie[team][year] = pieman
        temp_off[team][year] = offman
        temp_def[team][year] = defman

pickle.dump(temp_off, open("off_rating_diff.p", "wb"))
pickle.dump(temp_def, open("def_rating_diff.p", "wb"))
pickle.dump(pace, open("pace_diff.p", "wb"))
pickle.dump(pie, open("pie_diff.p", "wb"))


teamid_dict = {'ATL': 1610612737, 'BKN': 1610612751, 'BOS': 1610612738, 'CHA': 1610612766, 'CHI': 1610612741,
               'CLE': 1610612739, 'DAL': 1610612742, 'DEN': 1610612743, 'DET': 1610612765, 'GSW': 1610612744,
               'HOU': 1610612745, 'IND': 1610612754, 'LAC': 1610612746, 'LAL': 1610612747, 'MEM': 1610612763,
               'MIA': 1610612748, 'MIL': 1610612749, 'MIN': 1610612750, 'NOP': 1610612740, 'NYK': 1610612752,
               'OKC': 1610612760, 'ORL': 1610612753, 'PHI': 1610612755, 'PHX': 1610612756, 'POR': 1610612757,
               'SAC': 1610612758, 'SAS': 1610612759, 'TOR': 1610612761, 'UTA': 1610612762, 'WAS': 1610612764,
               'NJN': 1610612751, 'SEA': 1610612760, 'NOH': 1610612740}

"""
homeboy = {2018: ['CHA', 'MIA', 'SAC', 'LAL', 'MIN', 'DAL', 'MEM', 'NOP', 'WAS', 'ATL', 'CHI', 'CLE', 'PHX', 'NYK'],
             2017: ['WAS', 'LAC', 'DET', 'CHA', 'LAL', 'NYK', 'BKN', 'CHI', 'SAC', 'ORL', 'ATL', 'DAL', 'MEM', 'PHX'],
             2016: ['MIA', 'DEN', 'DET', 'CHA', 'NOP', 'DAL', 'SAC', 'MIN', 'NYK', 'ORL', 'PHI', 'LAL', 'PHX', 'BKN'],
             2015: ['CHI', 'WAS', 'UTA', 'ORL', 'DEN', 'MIL', 'SAC', 'NYK', 'NOP', 'MIN', 'PHX', 'BKN', 'LAL', 'PHI'],
             2014: ['OKC', 'PHX', 'IND', 'UTA', 'MIA', 'CHA', 'DET', 'DEN', 'SAC', 'ORL', 'LAL', 'PHI', 'NYK', 'MIN'],
             2013: ['PHX', 'MIN', 'NYK', 'DEN', 'NOP', 'CLE', 'DET', 'SAC', 'LAL', 'BOS', 'UTA', 'ORL', 'PHI', 'MIL'],
             2012: ['UTA', 'DAL', 'PHI', 'TOR', 'POR', 'MIN', 'DET', 'WAS', 'SAC', 'NOH', 'PHX', 'CLE', 'CHA', 'ORL'],
             2011: ['HOU', 'PHX', 'MIL', 'POR', 'MIN', 'DET', 'GSW', 'TOR', 'NJN', 'SAC', 'CLE', 'NOH', 'WAS', 'CHA'],
             2010: ['HOU', 'PHX', 'UTA', 'GSW', 'MIL', 'CHA', 'LAC', 'DET', 'NJN', 'SAC', 'WAS', 'TOR', 'CLE', 'MIN'],
             2009: ['HOU', 'MEM', 'TOR', 'NOH', 'IND', 'LAC', 'NYK', 'DET', 'PHI', 'GSW', 'WAS', 'SAC', 'MIN', 'NJN'],
             2008: ['PHX', 'IND', 'CHA', 'MIL', 'NJN', 'TOR', 'NYK', 'GSW', 'MEM', 'MIN', 'OKC', 'LAC', 'WAS', 'SAC'],
             2007: ['GSW', 'POR', 'SAC', 'IND', 'NJN', 'CHI', 'CHA', 'MIL', 'LAC', 'NYK', 'MEM', 'MIN', 'SEA', 'MIA']}

for year in homeboy:
    for i in range(len(homeboy[year])):
        homeboy[year][i] =teamid_dict[homeboy[year][i]]
print(homeboy)
for year in homeboy:
    homeboy[year].reverse()
print(homeboy)
pickle.dump(homeboy, open("lottery_teams.p", "wb"))
"""

"""
new_pace = {2007: {},
                      2008: {},
                      2009: {},
                      2010: {},
                      2011: {},
                      2012: {},
                      2013: {},
                      2014: {},
                      2015: {},
                      2016: {},
                      2017: {},
                      2018: {}}
new_pie = {2007: {},
              2008: {},
              2009: {},
              2010: {},
              2011: {},
              2012: {},
              2013: {},
              2014: {},
              2015: {},
              2016: {},
              2017: {},
              2018: {}}

new_pace = {}
new_pie = {}
for year in pace_pie:
    for team in pace_pie[year]:
        if teamid_dict[team] not in new_pace:
            new_pace[teamid_dict[team]] = {year: []}
            new_pace[teamid_dict[team]][year] = [i[0] for i in pace_pie[year][team]]
            new_pace[teamid_dict[team]][year].reverse()
            new_pie[teamid_dict[team]] = {year: []}
            new_pie[teamid_dict[team]][year] = [i[1] for i in pace_pie[year][team]]
            new_pie[teamid_dict[team]][year].reverse()
        else:
            new_pace[teamid_dict[team]][year] = [i[0] for i in pace_pie[year][team]]
            new_pace[teamid_dict[team]][year].reverse()
            new_pie[teamid_dict[team]][year] = [i[1] for i in pace_pie[year][team]]
            new_pie[teamid_dict[team]][year].reverse()

for team in temp_off:
    for year in temp_off[team]:
        temp_off[team][year].reverse()
        temp_def[team][year].reverse()

pickle.dump(temp_off, open("off_rating.p", "wb"))
pickle.dump(temp_def, open("def_rating.p", "wb"))
pickle.dump(new_pace, open("pace.p", "wb"))
pickle.dump(new_pie, open("pie.p", "wb"))

"""
"""
for year in off_def_rating:
    for team in off_def_rating[year]:
        off_rating[year][team] = [i[0] for i in off_def_rating[year][team]]
        def_rating[year][team] = [i[1] for i in off_def_rating[year][team]]
temp_off = {}
temp_def = {}
for year in off_rating:
    for team in off_rating[year]:
        if team not in temp_off:
            temp_off[team] = {year: []}
            temp_def[team] = {year: []}
            temp_off[team][year] = off_rating[year][team]
            temp_def[team][year] = def_rating[year][team]
        else:
            temp_off[team][year] = off_rating[year][team]
            temp_def[team][year] = def_rating[year][team]

for team in temp_off:
    for year in temp_off[team]:
"""
# pickle.dump(temp_off, open("off_rating.p", "wb"))
# pickle.dump(temp_def, open("def_rating.p", "wb"))





"""
teamid_dict = {'ATL': 1610612737, 'BKN': 1610612751, 'BOS': 1610612738, 'CHA': 1610612766, 'CHI': 1610612741,
               'CLE': 1610612739, 'DAL': 1610612742, 'DEN': 1610612743, 'DET': 1610612765, 'GSW': 1610612744,
               'HOU': 1610612745, 'IND': 1610612754, 'LAC': 1610612746, 'LAL': 1610612747, 'MEM': 1610612763,
               'MIA': 1610612748, 'MIL': 1610612749, 'MIN': 1610612750, 'NOP': 1610612740, 'NYK': 1610612752,
               'OKC': 1610612760, 'ORL': 1610612753, 'PHI': 1610612755, 'PHX': 1610612756, 'POR': 1610612757,
               'SAC': 1610612758, 'SAS': 1610612759, 'TOR': 1610612761, 'UTA': 1610612762, 'WAS': 1610612764,
               'NJN': 1610612751, 'SEA': 1610612760, 'NOH': 1610612740}

dict = {
2007: ['IND', 'NJN', 'CHI', 'CHA', 'MIL', 'NYK', 'MIA', 'GSW', 'POR', 'SAC', 'LAC', 'MIN', 'MEM', 'SEA'],
2008: ['IND', 'CHA', 'NJN', 'MIL', 'TOR', 'NYK', 'WAS', 'PHX', 'GSW', 'MIN', 'MEM', 'OKC', 'LAC', 'SAC'],
2009: ['TOR', 'IND', 'NYK', 'PHI', 'DET', 'WAS', 'NJN', 'HOU', 'MEM', 'NOH', 'LAC', 'GSW', 'SAC', 'MIN'],
2010: ['MIL', 'CHA', 'DET', 'NJN', 'WAS', 'TOR', 'CLE', 'HOU', 'PHX', 'UTA', 'GSW', 'LAC', 'SAC', 'MIN'],
2011: ['MIL', 'DET', 'TOR', 'NJN', 'CLE', 'WAS', 'CHA', 'HOU', 'PHX', 'POR', 'MIN', 'GSW', 'SAC', 'NOH'],
2012: ['PHI', 'TOR', 'DET', 'WAS', 'CLE', 'CHA', 'ORL', 'UTA', 'DAL', 'POR', 'MIN', 'SAC', 'NOH', 'PHX'],
2013: ['NYK', 'CLE', 'DET', 'BOS', 'ORL', 'PHI', 'MIL', 'PHX', 'MIN', 'DEN', 'NOP', 'SAC', 'LAL', 'UTA'],
2014: ['IND', 'MIA', 'CHA', 'DET', 'ORL', 'PHI', 'NYK', 'OKC', 'PHX', 'UTA', 'DEN', 'SAC', 'LAL', 'MIN'],
2015: ['CHI', 'WAS', 'ORL', 'MIL', 'NYK', 'BKN', 'PHI', 'UTA', 'SAC', 'DEN', 'NOP', 'MIN', 'PHX', 'LAL'],
2016: ['MIA', 'DET', 'CHA', 'NYK', 'ORL', 'PHI', 'BKN', 'DEN', 'NOP', 'DAL', 'SAC', 'MIN', 'LAL', 'PHX'],
2017: ['DET', 'CHA', 'NYK', 'BKN', 'CHI', 'ORL', 'ATL', 'DEN', 'LAC', 'LAL', 'SAC', 'DAL', 'MEM', 'PHX'],
2018: ['CHA', 'MIA', 'WAS', 'ATL', 'CHI', 'CLE', 'NYK', 'SAC', 'LAL', 'MIN', 'MEM', 'NOP', 'DAL', 'PHX'],
}


for year in dict:
    for i in range(len(dict[year])):
        dict[year][i] = teamid_dict[dict[year][i]]

pickle.dump(dict, open("lottery_teams.p", "wb"))



"""



"""
for team in weighted_age_bygame_reformat:
    print(team)
    for year in weighted_age_bygame_reformat[team]:
        print(len(weighted_age_bygame_reformat[team][year]))
"""

"""
player_dob_hash = pickle.load(open("player_dob_hash.p", "rb"))

url = "https://stats.nba.com/player/"
for player_id in player_dob_hash:
    if type(player_dob_hash[player_id]) == float:
        temp_url = url + str(player_id) + "/"
        page = requests.get(temp_url)
        tree = html.fromstring(page.content)
        dob = tree.xpath('/html/body/main/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[4]/span/text()')
        dob = dob[0].split('/')
        str_dob = dob[2] + '-' + dob[0] + '-' + dob[1]
        player_dob_hash[player_id] = str_dob
        print(str_dob)


pickle.dump(player_dob_hash, open("player_dob_hash.p", "wb"))
"""