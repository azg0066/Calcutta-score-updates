import requests
import json



'''The purpose of this file is to 
    a) generate a list of "short team names" that the Henrygd NCAA API pulls so I can accurately input them into the contestants' lists of acquired teams. 
    b) Check the contestants' team lists to ensure the names are input correctly
    c) Check the other way around, to make sure that all names pulled by the API are present in some list. 

'''


''' the below URLs pull the team names from every game in day day 1 and day 2, i.e., all teams in the tourney.'''
url1 = "http://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2026/03/19" #day 1 games
url2 = "http://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2026/03/20" #day 2 games

WIL_TEAMS = ['UCLA','South Fla.', 'California Baptist', 'North Dakota St.', "Furman", "Siena", "Arizona", "Arkansas", "BYU", "Utah St.", "Missouri", "Michigan", "Kentucky", "Saint Louis", "Santa Clara", "Akron", "Hofstra", "Wright St.", "Tennessee St.", "Howard", "Florida", "Texas A&M", "VCU", "McNeese"]
WES_TEAMS = ['Michigan St.', 'Kansas', 'Louisville', 'Ohio St.', 'UCF', 'Gonzaga', 'Wisconsin', 'Miami (FL)', 'Villanova', 'Texas', 'Alabama', 'Tennessee', 'Houston', 'Nebraska', 'North Carolina', "Saint Mary's (CA)", 'Iowa']
CHASE_TEAMS = ['Duke', 'UConn', "St. John's (NY)", 'TCU', 'UNI', 'Purdue', 'High Point', 'Hawaii', 'Kennesaw St.', 'Queens (NC)', 'LIU', 'Iowa St.', 'Virginia', 'Texas Tech', 'Georgia', 'Miami (OH)', 'Illinois', 'Vanderbilt', 'Clemson', 'Troy', 'Penn', 'Idaho', 'Prairie View']
COMBINED_CONTESTANT_TEAM_LIST = WIL_TEAMS + WES_TEAMS + CHASE_TEAMS



data = json.loads(requests.get(url=url1).content) + json.loads(requests.get(url=url2).content)

team_list = []

for game in data["games"]:
    team_list.append(game["game"]["home"]["names"]["short"])
    team_list.append(game["game"]["away"]["names"]["short"])

team_list.sort()

with open("team_list.txt", 'w') as f:
    f.write('\n'.join(map(str,team_list)))


'''the below block checks if the teams chosen by the contestants match the names presented in the raw data'''

for team in COMBINED_CONTESTANT_TEAM_LIST:
    if team not in team_list:
        print(team)

'''The below block checks if all teams in the raw data are present in the contestant lists'''

for team in team_list:
    if team not in COMBINED_CONTESTANT_TEAM_LIST:
        print(team)