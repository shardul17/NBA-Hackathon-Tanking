from selenium import webdriver
from pandas import *
import pandas
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import *
import pickle


path_to_chromedriver = 'chromedriver.exe' # Path to access a chrome driver
browser = webdriver.Chrome(executable_path=path_to_chromedriver)

# url = 'https://stats.nba.com/lineups/advanced/?Season=2018-19&SeasonType=Regular%20Season&sort=MIN&dir=1'
#
# browser.get(url)
#
#
# browser.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div/label/select/option[1]').click()
# browser.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select/option[1]').click()
#
# browser.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]').click()

# table = browser.find_element_by_class_name('nba-stat-table__overflow')
year = 2018
big_dict = {}
teams = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
         'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
         'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS',
         'NJN', 'SEA', 'NOH']


teamid_dict = {'ATL': 1610612737, 'BKN': 1610612751, 'BOS': 1610612738, 'CHA': 1610612766, 'CHI': 1610612741,
             'CLE': 1610612739, 'DAL': 1610612742, 'DEN': 1610612743, 'DET': 1610612765, 'GSW': 1610612744,
             'HOU': 1610612745, 'IND': 1610612754, 'LAC': 1610612746, 'LAL': 1610612747, 'MEM': 1610612763,
             'MIA': 1610612748, 'MIL': 1610612749, 'MIN': 1610612750, 'NOP': 1610612740, 'NYK': 1610612752,
             'OKC': 1610612760, 'ORL': 1610612753, 'PHI': 1610612755, 'PHX': 1610612756, 'POR': 1610612757,
             'SAC': 1610612758, 'SAS': 1610612759, 'TOR': 1610612761, 'UTA': 1610612762, 'WAS': 1610612764,
             'NJN': 1610612751, 'SEA': 1610612760, 'NOH': 1610612740}


for itr in range(2,14):
    if year >= 2009:
        temp_year = str(year) + "-" + str(int(str(year)[2:]) + 1)
    else:
        temp_year = str(year) + "-" + '0' + str(int(str(year)[2:]) + 1)


    url = 'https://stats.nba.com/lineups/advanced/?Season=' + temp_year + '&SeasonType=Regular%20Season&sort=MIN&dir=1'
    browser.get(url)

    browser.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div/label/select/option[1]').click()
    browser.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select/option[1]').click()


    table = browser.find_element_by_class_name('nba-stat-table__overflow')



    big_names = []
    big_stats = []

    count = 1
    for line_id, lines in enumerate(table.text.split('\n')):
        space_split = lines.split(" ")
        names = []
        stats = []

        end_index = 0
        for i in range(len(space_split)):
            if space_split[i] not in teams:
                names.append(space_split[i])
            else:
                end_index = i
                break

        for i in range(end_index, len(space_split)):
            stats.append(space_split[i])

        big_names.append(names)
        big_stats.append(stats)


    #temp_year = str(year )
    big_dict[temp_year] = {}
    column_names = ['TEAM', 'GP', 'MIN', 'OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'PACE', 'PIE']

    big_stats.pop(0)
    big_names.pop(0)


    for i in range(len(big_names)):

        name_string = ''
        for name in big_names[i]:
            name_string += name + " "
        if teamid_dict[big_stats[i][0]] not in big_dict[temp_year]:
            big_dict[temp_year][teamid_dict[big_stats[i][0]]] = {}
            big_dict[temp_year][teamid_dict[big_stats[i][0]]][name_string] = {}
            for j in range(1, len(column_names)):
                big_dict[temp_year][teamid_dict[big_stats[i][0]]][name_string][column_names[j]] = big_stats[i][j]
                #print(big_dict)
        else:
            big_dict[temp_year][teamid_dict[big_stats[i][0]]][name_string] = {}
            for j in range(1, len(column_names)):
                big_dict[temp_year][teamid_dict[big_stats[i][0]]][name_string][column_names[j]] = big_stats[i][j]
                #print(big_dict)



    year -= 1
    #browser.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[' + str(itr) + "]").click()
    print(big_dict)




#pickle.dump(big_dict, open("lineup_data.p", "wb"))
