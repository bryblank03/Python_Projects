
import numpy as np
import pandas as pd
import random
import time
from unidecode import unidecode

teams = [ 'atl', 'bos' , 'brk', 'cha', 'chi', 'cle', 'dal', 'den', 'det', 'gsw', 'hou', 'ind', 'lac', 'lal', 'mem', 'mia', 'mil', 'min', 'nop', 'nyk', 'okc', 'orl', 'phi', 'pho', 'por', 'sac', 'sas', 'tor', 'uta', 'was']
len(teams)
seasons = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
len(seasons)
stats = [ 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF']

tm_stats_dict = {stat: 'Tm_' + str(stat) for stat in stats}

opp_stats_dict = {stat + '.1' : 'Opp_' + str(stat) for stat in stats}

nba_df = pd.DataFrame()
for season in seasons:
    for team in teams:
        url = 'https://www.basketball-reference.com/teams/' + team + '/' + season + '/gamelog/'
        print(url)
        try:
            team_df = pd.read_html(url, header=1, attrs={'id':'tgl_basic'})[0]
        except Exception as e:
            print(f"Failed to fetch data for {team} in {season}. Error: {e}")
            continue
        team_df = team_df[(team_df['Rk'].str != '') & (team_df['Rk'].str.isnumeric())]
        team_df = team_df.drop(columns=['Rk','Unnamed: 24'])

        team_df = team_df.rename(columns={'Unnamed: 3':'Home', 'Tm':'Tm_Pts', 'Opp.1':'Opp_Pts'})
        team_df = team_df.rename(columns=tm_stats_dict)
        team_df = team_df.rename(columns=opp_stats_dict)

        team_df['Home'] = team_df['Home'].apply(lambda x: 0 if x == '@' else 1)
        
        team_df.insert(loc=0, column='Season', value=season)
        team_df.insert(loc=1, column='Team', value=team.upper())

        nba_df = pd.concat([nba_df, team_df], ignore_index=True)

        time.sleep(random.randint(6, 9))

print(nba_df)

nba_df.to_csv('nba-gamelogs-2014-2023.csv', index=False)