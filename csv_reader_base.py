import gzip
import pandas as pd
import pickle
from pprint import pprint


player_map = pickle.load(open("player_map.p", "rb"))
game_map_dates = pickle.load(open("game_map_dates.p", "rb"))
game_map = pickle.load(open("game_map.p", "rb"))


with open('Box_Scores.csv', 'rb') as fd:
    gzip_fd = gzip.GzipFile(fileobj=fd)
    print(gzip_fd)
    data = pd.read_csv(gzip_fd,header=0,encoding = 'unicode_escape')


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)
print(data.head())


"""
point_diff = {}
for x, row in data.iterrows():
    if game_map[row['Game_id']] < 2007:
        continue
    else:
        if row['Game_id'] not in point_diff:
            point_diff[row['Game_id']] = {row['Team_id']: row['Points']}
        elif row['Team_id'] not in point_diff[row['Game_id']]:
            point_diff[row['Game_id']][row['Team_id']] = row['Points']
        else:
            point_diff[row['Game_id']][row['Team_id']] += row['Points']

print(point_diff)
#pickle.dump(point_diff, open("margin_of_v.p", "wb"))

point_diff_ref = {}
for game in point_diff:
    for team in point_diff[game]:
        if team not in point_diff_ref:
            point_diff_ref[team] ={}
            point_diff_ref[team][game_map[game]] = []
            team_list = list(point_diff[game].keys())
            if team == team_list[0]:
                temp_diff = point_diff[game][team] - point_diff[game][team_list[1]]
            else:
                temp_diff = point_diff[game][team] - point_diff[game][team_list[0]]

            if len(point_diff_ref[team][game_map[game]]) < 82 and game_map[game] != 2011:
                point_diff_ref[team][game_map[game]].append(temp_diff)
            elif len(point_diff_ref[team][game_map[game]]) < 66 and game_map[game] == 2011:
                point_diff_ref[team][game_map[game]].append(temp_diff)
        elif game_map[game] not in point_diff_ref[team]:
            point_diff_ref[team][game_map[game]] = []
            team_list = list(point_diff[game].keys())
            if team == team_list[0]:
                temp_diff = point_diff[game][team] - point_diff[game][team_list[1]]
            else:
                temp_diff = point_diff[game][team] - point_diff[game][team_list[0]]

            if len(point_diff_ref[team][game_map[game]]) < 82 and game_map[game] != 2011:
                point_diff_ref[team][game_map[game]].append(temp_diff)
            elif len(point_diff_ref[team][game_map[game]]) < 66 and game_map[game] == 2011:
                point_diff_ref[team][game_map[game]].append(temp_diff)
        else:
            team_list = list(point_diff[game].keys())
            if team == team_list[0]:
                temp_diff = point_diff[game][team] - point_diff[game][team_list[1]]
            else:
                temp_diff = point_diff[game][team] - point_diff[game][team_list[0]]


            if len(point_diff_ref[team][game_map[game]]) < 82 and game_map[game] != 2011:
                point_diff_ref[team][game_map[game]].append(temp_diff)
            elif len(point_diff_ref[team][game_map[game]]) < 66 and game_map[game] == 2011:
                point_diff_ref[team][game_map[game]].append(temp_diff)

pprint(point_diff_ref)
pickle.dump(point_diff_ref, open("margin_of_v.p", "wb"))
"""


"""
weighted_minutes = {}

for x, row_data in data.iterrows():
    if row_data['Game_id'] not in weighted_minutes:
        weighted_minutes[row_data['Game_id']] = {'Game Date': game_map_dates[row_data['Game_id']], row_data['Team_id']: {}}
        weighted_minutes[row_data['Game_id']][row_data['Team_id']][row_data['Person_id']] = row_data['minutes']
    elif row_data['Team_id'] not in weighted_minutes[row_data['Game_id']]:
        weighted_minutes[row_data['Game_id']][row_data['Team_id']] = {}
        weighted_minutes[row_data['Game_id']][row_data['Team_id']][row_data['Person_id']] = row_data['minutes']
    else:
        weighted_minutes[row_data['Game_id']][row_data['Team_id']][row_data['Person_id']] = row_data['minutes']
pprint(weighted_minutes)

pickle.dump(weighted_minutes, open("weighted_minutes.p", "wb"))
"""

"""
player_dob_hash = {}
for x, row_data in data.iterrows():
    if row_data['Person_ID'] in player_dob_hash:
        continue
    elif row_data['Season'] > 2006 and row_data['Person_ID'] in player_map:
        player_dob_hash[row_data['Person_ID']] = row_data['Birthdate']

pprint(player_dob_hash)
"""



"""
for x,row_data in data.iterrows():
    year = game_map[row_data['Game_id']]

    if year >= 2007:
        if row_data['Person_id'] not in player_map:
        if row_data['Person_id'] not in player_map:
            if row_data["Person_id"] not in absent_players:
                absent_players.append(row_data['Person_id'])
            continue

        if row_data['Period'] == 0 and row_data['status'] == 'A' and year != 2002:
            if year not in active_lineups:
                active_lineups[year] = {}
            if row_data['Game_id'] not in active_lineups[year]:
                active_lineups[year][row_data['Game_id']] = {}
            if row_data["Team_id"] not in active_lineups[year][row_data["Game_id"]]:
                active_lineups[year][row_data["Game_id"]][row_data['Team_id']] = [player_map[row_data["Person_id"]]]
            else:
                active_lineups[year][row_data["Game_id"]][row_data['Team_id']].append(player_map[row_data["Person_id"]])


print(active_lineups)

print(absent_players)
print(len(absent_players))




# for i in range(50):
#     print(data.iloc[i])

pickle.dump(active_lineups, open("active_lineups.p", "wb"))
"""