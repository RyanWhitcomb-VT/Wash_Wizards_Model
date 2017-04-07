# STAT 4214
# Scrape Wizards Data
# 4-6-17

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Get HTML code for the page
url = 'http://www.basketball-reference.com/teams/WAS/2017_games.html'
page = requests.get(url).content
soup = BeautifulSoup(page, "lxml")
rows = soup.find_all('tr')

# Set up the lists to contain the data
ast = []
reb = []
fga = []
fgp = []
turn = []
ftp = []
fta = []
ortg = []
home = []
conf = []
ot = []
pts = []

# Get all the box scores
games = []
for row in rows:
    try:
        game = row.find_all('td')[3].find('a', href=True)['href']
        games.append(game)
        if row.find_all('td')[4].text.encode('ascii','replace') == '@':
            home.append(0)
        else:
            home.append(1)
        if row.find_all('td')[7].text.encode('ascii','replace') == 'OT':
            ot.append(0)
        else:
            ot.append(1) 
    except IndexError:
        continue
    
# Extract statistics
stats_url = 'http://www.basketball-reference.com'
for game in games:
    game_url = stats_url + game
    stats_page = requests.get(game_url).content
    stats_soup = BeautifulSoup(stats_page, "lxml")
    tables = stats_soup.find_all('table')
    for idx, table in enumerate(tables):
        if table.caption.text.encode('ascii','replace')[0:18] == 'Washington Wizards':
            totals = table.find_all('tr')[-1]
            fga.append(int(totals.find_all('td')[2].text))
            fgp.append(float(totals.find_all('td')[3].text))
            fta.append(int(totals.find_all('td')[8].text))
            ftp.append(float(totals.find_all('td')[9].text))
            reb.append(int(totals.find_all('td')[12].text))
            ast.append(int(totals.find_all('td')[13].text))
            turn.append(int(totals.find_all('td')[16].text))
            pts.append(int(totals.find_all('td')[18].text))
            
            totals = tables[idx + 1]
            ortg.append(float(totals.find_all('td')[13].text))
            print int(totals.find_all('td')[13].text)
    
# Create DataFrame
df = pd.DataFrame()
df['Assists'] = ast
df['Rebounds'] = reb
df['Field Goals Attempted'] = fga
df['Field Goal Percentage'] = fgp
df['Turnovers'] = turn
df['Free Throws Attempted'] = fta
df['Free Throw Percentage'] = ftp
df['Offensive Rating'] = ortg
#df['Home or Away'] = home
#df['Conference'] = conf
#df['Overtime'] = ot
df['Points'] = pts

df.to_csv('wizards_data.csv')