import gzip
import pandas as pd
import pickle
from pprint import pprint



new_player_map = pickle.load(open("new_player_map.p", "rb"))
game_map = pickle.load(open("game_map.p", "rb"))
golden_lineup = pickle.load(open("golden_lineup.p", "rb"))
#golden_minutes = pickle.load(open("golden_minutes.p", "rb"))
new_player_map[699] = '.B. Barry'

print(new_player_map)
"""
for id in player_map:
    name = ''
    ind_name_list = player_map[id].split(" ")
    if len(ind_name_list) == 1:
        name = '.' + ind_name_list[0]
    elif len(ind_name_list) == 2:
        name = '.' + ind_name_list[0][0] + '. ' + ind_name_list[1]
    elif len(ind_name_list) == 3:
        name = '.' + ind_name_list[0][0] + '. ' + ind_name_list[1] + ' ' + ind_name_list[2]
    new_player_map[id] = name

pickle.dump(new_player_map, open("new_player_map.p", "wb"))
"""






with open('Box_Scores.csv', 'rb') as fd:
    gzip_fd = gzip.GzipFile(fileobj=fd)
    print(gzip_fd)
    data = pd.read_csv(gzip_fd,header=0,encoding = 'unicode_escape')

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

print(data.head())

golden_minutes = {}

for x,row_data in data.iterrows():
    if row_data['Game_id'] in golden_lineup:
        if row_data['Game_id'] not in golden_minutes:
            golden_minutes[row_data['Game_id']] = {}
        for team in golden_lineup[row_data['Game_id']]:
            if team not in golden_minutes[row_data['Game_id']]:
                golden_minutes[row_data['Game_id']][team] = 0
            if row_data['Person_id'] not in new_player_map:
                print(row_data['Person_id'], row_data['minutes'])
                #print(row_d)
            elif new_player_map[row_data['Person_id']] in golden_lineup[row_data['Game_id']][team]:
                #print('hey')
                golden_minutes[row_data['Game_id']][team] += row_data['minutes']

print(golden_minutes)



for game in golden_minutes:
    for team in golden_minutes[game]:
        golden_minutes[game][team] = golden_minutes[game][team]/(48*5)

print(golden_minutes)
# pickle.dump(golden_minutes, open("golden_minutes.p", "wb"))



