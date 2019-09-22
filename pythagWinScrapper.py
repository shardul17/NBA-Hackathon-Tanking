from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas
import numpy as np
import pickle


# 2008
teams1 = ['ATL', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
          'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NYK',
          'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS',
          'NJN', 'SEA', 'NOH']

# 2009 - 2012
teams2 = ['ATL', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET',
          'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN',
          'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR',
          'UTA', 'WAS', 'NJN', 'NOH']

# 2013
teams3 = ['ATL', 'BOS', 'BRK', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET',
          'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN',
          'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR',
          'UTA', 'WAS', 'NOH']

# 2014
teams4 = ['ATL', 'BOS', 'BRK', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET',
          'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN',
          'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR',
          'UTA', 'WAS', 'NOP']

# 2015 - 2019
teams5 = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET',
          'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN',
          'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR',
          'UTA', 'WAS', 'NOP']

my_dict = {}
teamid_dict = {'ATL': 1610612737, 'BRK': 1610612751, 'BOS': 1610612738, 'CHA':1610612766, 'CHO': 1610612766, 'CHI': 1610612741,
               'CLE': 1610612739, 'DAL': 1610612742, 'DEN': 1610612743, 'DET': 1610612765, 'GSW': 1610612744,
               'HOU': 1610612745, 'IND': 1610612754, 'LAC': 1610612746, 'LAL': 1610612747, 'MEM': 1610612763,
               'MIA': 1610612748, 'MIL': 1610612749, 'MIN': 1610612750, 'NOP': 1610612740, 'NYK': 1610612752,
               'OKC': 1610612760, 'ORL': 1610612753, 'PHI': 1610612755, 'PHO': 1610612756, 'POR': 1610612757,
               'SAC': 1610612758, 'SAS': 1610612759, 'TOR': 1610612761, 'UTA': 1610612762, 'WAS': 1610612764,
               'NJN': 1610612751, 'SEA': 1610612760, 'NOH': 1610612740}

def add_to_my_dict(team, year, data):
    global my_dict
    if team not in my_dict:
        my_dict[team] = {}
    if year not in my_dict[team]:
        my_dict[team][year] = {}
    my_dict[team][year] = data

for i in range(len(teams1)):
    for year in range(2008, 2020):
        if year == 2008:
            url = "https://www.basketball-reference.com/teams/" + teams1[i] + "/" + str(year) + "_games.html"
        elif (year >= 2009) & (year <= 2012):
            url = "https://www.basketball-reference.com/teams/" + teams2[i] + "/" + str(year) + "_games.html"
        elif year == 2013:
            url = "https://www.basketball-reference.com/teams/" + teams3[i] + "/" + str(year) + "_games.html"
        elif year == 2014:
            url = "https://www.basketball-reference.com/teams/" + teams4[i] + "/" + str(year) + "_games.html"
        elif (year >= 2015) & (year <= 2019):
            url = "https://www.basketball-reference.com/teams/" + teams5[i] + "/" + str(year) + "_games.html"
        print(url)
        html = urlopen(url)
        soup = BeautifulSoup(html)

        # set up dataframe
        soup.findAll('tr', limit=2)
        headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        headers = headers[1:]
        rows = soup.findAll('tr')[1:]
        team_stats = [[td.getText() for td in rows[i].findAll('td')]
                      for i in range(len(rows))]
        stats = pandas.DataFrame(team_stats, columns=headers)
        stats.columns = ["Date", "Start(ET)", "Blank1", "Blank2", "Blank3", "Opponent", "Win, Loss",
                         "OT", "Tm", "Opp", "W", "L", "Streak", "Notes"]
        stats = stats.replace(to_replace='None', value=np.nan, inplace=False).dropna()
        stats = stats.replace(to_replace=['L', 'W'], value=[0, 1])
        stats.astype({'Tm': 'int64'}).dtypes
        stats.astype({'Opp': 'int64'}).dtypes
        stats = stats.head(82)
        tmL = stats['Tm'].rolling(10, center=True, min_periods=5).sum().tolist()
        OppL = stats['Opp'].rolling(10, center=True, min_periods=5).sum().tolist()
        WinsL = stats['Win, Loss'].rolling(10, center=True, min_periods=5).sum().tolist()

        # 13.91 is the pythagorean exponent
        newL = (np.power(tmL, 13.91)) / (np.power(tmL, 13.91) + np.power(OppL, 13.91))
        # 16.5 is the pythagorean exponent
        # newL = (np.power(tmL, 16.5))/(np.power(tmL, 16.5)+np.power(OppL, 16.5))

        # adjust win % to # of wins
        for j in range(len(newL)):
            if j == 0:
                newL[j] = newL[j] * 5
            elif j == 1:
                newL[j] = newL[j] * 6
            elif j == 2:
                newL[j] = newL[j] * 7
            elif j == 3:
                newL[j] = newL[j] * 8
            elif j == 4:
                newL[j] = newL[j] * 9
            elif j == 78:
                newL[j] = newL[j] * 9
            elif j == 79:
                newL[j] = newL[j] * 8
            elif j == 80:
                newL[j] = newL[j] * 7
            elif j == 81:
                newL[j] = newL[j] * 6
            else:
                newL[j] = newL[j] * 10

        pythDiff = WinsL - newL

        if year == 2008:
            add_to_my_dict(teamid_dict[teams1[i]], year, pythDiff)
            #my_dict[teams1[i] + "/" + str(year)] = pythDiff
        elif (year >= 2009) & (year <= 2012):
            add_to_my_dict(teamid_dict[teams2[i]], year, pythDiff)
            #my_dict[teams2[i] + "/" + str(year)] = pythDiff
        elif year == 2013:
            add_to_my_dict(teamid_dict[teams3[i]], year, pythDiff)
            #my_dict[teams3[i] + "/" + str(year)] = pythDiff
        elif year == 2014:
            add_to_my_dict(teamid_dict[teams4[i]], year, pythDiff)
            #my_dict[teams4[i] + "/" + str(year)] = pythDiff
        elif (year >= 2015) & (year <= 2019):
            add_to_my_dict(teamid_dict[teams5[i]], year, pythDiff)
            #my_dict[teams5[i] + "/" + str(year)] = pythDiff

pickle.dump(my_dict, open("pythag_win_differential.p", "wb"))