import pickle
from pprint import pprint

"""team_map = pickle.load(open('final_data_pickles/pythag_win_differential.p', 'rb'))
new_team_map = {}
for team in team_map:
    new_team_map[team] = {}
    for year in team_map[team].keys():
        temp_year = year - 1
        new_team_map[team][temp_year] = team_map[team][year]

pickle.dump(new_team_map, open('final_data_pickles/pythag_win_differential.p', 'wb'))"""

win_loss = pickle.load(open('final_data_pickles/pace.p', 'rb'))
pprint(win_loss)
