import requests
import json
import time 
import traceback
import datetime


url1 = "http://localhost:3000/scoreboard/basketball-men/d1/2025/03/20"
url2 = "http://localhost:3000/scoreboard/basketball-men/d1/2025/03/21"
url3 = "http://localhost:3000/scoreboard/basketball-men/d1/2025/03/22"
url4 = "http://localhost:3000/scoreboard/basketball-men/d1/2025/03/23"
url5 = "http://localhost:3000/scoreboard/basketball-men/d1/2025/03/27"
url6 = "http://localhost:3000/scoreboard/basketball-men/d1/2025/03/28"
url7 = "http://localhost:3000/scoreboard/basketball-men/d1/2025/03/29"
url8 = "http://localhost:3000/scoreboard/basketball-men/d1/2025/03/30"
url9 = "http://localhost:3000/scoreboard/basketball-men/d1/2025/04/05"
url10 = "http://localhost:3000/scoreboard/basketball-men/d1/2025/04/07"




discord_url = "https://discord.com/api/v9/channels/1353045468153905227/messages"
auth = {'authorization': "Njk2MjEyOTI5MTE2MjQxOTIw.GoYHLq.52sqnZj1aybn2vA2o3QfmI2dYuNQwQjRdzKiP8"}


RD1_WIN = 3.065
RD2_WIN = 7.663
RD3_WIN = 21.455
RD4_WIN = 30.65
RD5_WIN = 22.988
RD6_WIN = 39.845


ABHI_TEAMS = ['Florida','Duke', 'VCU', 'Colorado St.', "Michigan St.", "Louisville", "Creighton", "New Mexico", "North Carolina", "UC San Diego", "Yale", "Lipscomb", "Bryant", "Alabama St.", "Tennessee", "Clemson"]
CAROL_TEAMS = [ "Oregon", "Mississippi St.", "Liberty", "Florida", "Arkansas", "Grand Canyon", "UNC Wilmington", "Omaha", "Norfolk St.", "Iowa St.", "Michigan", "Ole Miss", "Houston", "Purdue", "Illinois", "UCLA", "Utah St.", "McNeese", "High Point", "Troy", "Wofford", "SIU Edwardsville"]
WES_TEAMS = ["Gonzaga", 'Maryland',"Wisconsin", "BYU", "Saint Mary's (CA)", "Missouri", "Oklahoma", "Drake", "Auburn", "Georgia"]
CHASE_TEAMS = ["Alabama", "Arizona", "Baylor", "Vanderbilt", "Akron", "Montana", "Robert Morris", "Mount St. Mary's", "St. John's (NY)", "Texas Tech", "Memphis", "Kansas", "UConn", "Texas A&M", "Marquette", "Kentucky", "Xavier"]


master_dictionary = {'Abhi':{'total': 0}, "Carol":{'total':0}, "Wes":{'total':0}, "Chase": {'total':0}}


def is_final(game):
    if game['game']['finalMessage']=='FINAL' or game['game']['finalMessage'] == 'FINAL (OT)':
        return True
    else:
        return False

def get_winner(game):
    round = game['game']['bracketRound']
    if(round=="First Round"):
        round = 1
    elif(round=="Second Round"):
        round = 2
    elif(round=="Sweet 16"):
        round = 3
    elif(round=="Elite Eight"):
        round = 4
    elif(round=="Final Four"):
        round = 5
    elif(round=="Championship"):
        round = 6


    winner_round = {'round': round}
    if (game['game']['away']['winner']):
        winner = game['game']['away']['names']['short']
    else:
        winner = game['game']['home']['names']['short']

    winner_round['winner'] = winner
    return winner_round

def search_assignments(winner_list):
    for winner_round in winner_list:
        round = winner_round['round']
        winner = winner_round['winner']
        for player in master_dictionary:
            for team in master_dictionary[player]:
                if team == winner:
                    master_dictionary[player][team][round-1] =1

def update_totals():
    for player in master_dictionary:
        for team in master_dictionary[player]:
            if team == 'total': 
                continue
                      
            if master_dictionary[player][team][5] == 1:
                if team == 'Florida':
                    master_dictionary[player]['total'] += RD6_WIN/2
                else:
                    master_dictionary[player]['total'] += RD6_WIN
            if master_dictionary[player][team][4] == 1:
                if team == 'Florida':
                    master_dictionary[player]['total'] += RD5_WIN/2
                else:
                    master_dictionary[player]['total'] += RD5_WIN
            if master_dictionary[player][team][3] == 1:
                if team == 'Florida':
                    master_dictionary[player]['total'] += RD4_WIN/2
                else:
                    master_dictionary[player]['total'] += RD4_WIN
            if master_dictionary[player][team][2] == 1:
                if team == 'Florida':
                    master_dictionary[player]['total'] += RD3_WIN/2
                else:
                    master_dictionary[player]['total'] += RD3_WIN
            if master_dictionary[player][team][1] == 1:
                if team == 'Florida':
                    master_dictionary[player]['total'] += RD2_WIN/2
                else:
                    master_dictionary[player]['total'] += RD2_WIN
            if master_dictionary[player][team][0] == 1:
                if team == 'Florida':
                    master_dictionary[player]['total'] += RD1_WIN/2
                else:
                    master_dictionary[player]['total'] += RD1_WIN


                    
def setup():
    for team in ABHI_TEAMS:
        master_dictionary['Abhi'][team] = [0,0,0,0,0,0]
    for team in CAROL_TEAMS:
        master_dictionary['Carol'][team] = [0,0,0,0,0,0]
    for team in WES_TEAMS:
        master_dictionary['Wes'][team] = [0,0,0,0,0,0]
    for team in CHASE_TEAMS:
        master_dictionary['Chase'][team] = [0,0,0,0,0,0]    


def get_wins():
    rd1_wins = []
    rd2_wins = []
    rd3_wins = []
    for player in master_dictionary:
        if master_dictionary[player] == "total":
            continue
        


def main():
    setup()
    
    data = json.loads(requests.get(url=url1).content)
    data2 = json.loads(requests.get(url=url2).content)
    data3 = json.loads(requests.get(url=url3).content)
    data4 = json.loads(requests.get(url=url4).content)
    data5 = json.loads(requests.get(url=url5).content)
    data6 = json.loads(requests.get(url=url6).content)
    data7 = json.loads(requests.get(url=url7).content)
    data8 = json.loads(requests.get(url=url8).content)
    data9 = json.loads(requests.get(url=url9).content)
    data10 = json.loads(requests.get(url=url10).content)

    games_day1 = data["games"]
    games_day2 = data2["games"]
    games_day3 = data3["games"]
    games_day4 = data4["games"]
    games_day5 = data5["games"]
    games_day6 = data6["games"]
    games_day7 = data7["games"]
    games_day8 = data8["games"]
    games_day9 = data9["games"]
    games_day10 = data10["games"]

    winner_list = []
    
    for game in games_day1:
        if game['game']['bracketRound'] == '':
            break
        if (is_final(game)):
            winner_list.append(get_winner(game))
    for game in games_day2:
        if game['game']['bracketRound'] == '':
            break
        if (is_final(game)):
            winner_list.append(get_winner(game))
    for game in games_day3:
        if (is_final(game)):
            get_winner(game)['round'] = 2
            winner_list.append(get_winner(game))
    for game in games_day4:
        if game['game']['bracketRound'] == '':
            break
        if (is_final(game)):
            winner_list.append(get_winner(game))
    for game in games_day5:
        if game['game']['bracketRound'] == '':
            break
        if (is_final(game)):
            get_winner(game)['round'] = 3
            winner_list.append(get_winner(game))
    for game in games_day6:
        if game['game']['bracketRound'] == '':
            break
        if (is_final(game)):
            winner_list.append(get_winner(game))
    for game in games_day7:
        if game['game']['bracketRound'] == '':
            break
        if (is_final(game)):
            winner_list.append(get_winner(game))
    for game in games_day8:
        if game['game']['bracketRound'] == '':
            break
        if (is_final(game)):
            winner_list.append(get_winner(game))
    for game in games_day9:
        if game['game']['bracketRound'] == '':
            break
        if (is_final(game)):
            winner_list.append(get_winner(game))
    for game in games_day10:
        if game['game']['bracketRound'] == '':
            break
        if (is_final(game)):
            winner_list.append(get_winner(game))


    search_assignments(winner_list=winner_list)
    update_totals()

    scoreboard = 'LATEST SCOREBOARD as of ' + datetime.datetime.now().strftime("%H:%M") + " EST\n" 
    for player in master_dictionary:
        scoreboard += (player + " total: $" + str(round(master_dictionary[player]['total'],2)))
        scoreboard += ("\n" + player + " Round 1 wins: \n" )
        
        rd1_wins = []
        for game in master_dictionary[player]:
            if game == 'total':
                continue
            else:
                if (master_dictionary[player][game][0] == 1):
                    rd1_wins.append(game)
        scoreboard += str(rd1_wins) + "\n"

        rd2_wins = []
        for game in master_dictionary[player]:
            if game == 'total':
                continue
            else:
                if (master_dictionary[player][game][1] == 1):
                    rd2_wins.append(game)
        scoreboard += ("\n" + player + " Round 2 wins: " + "\n" + str(rd2_wins) + "\n") 

        rd3_wins = []
        for game in master_dictionary[player]:
            if game == 'total':
                continue
            else:
                if (master_dictionary[player][game][2] == 1):
                    rd3_wins.append(game)
        scoreboard += ("\n" + player + " Sweet Sixteen wins: " + "\n" + str(rd3_wins) + "\n\n")

        rd4_wins = []
        for game in master_dictionary[player]:
            if game == 'total':
                continue
            else:
                if (master_dictionary[player][game][3] == 1):
                    rd3_wins.append(game)
        scoreboard += ("\n" + player + " Elite Eight wins: " + "\n" + str(rd4_wins) + "\n\n")

        rd5_wins = []
        for game in master_dictionary[player]:
            if game == 'total':
                continue
            else:
                if (master_dictionary[player][game][4] == 1):
                    rd3_wins.append(game)
        scoreboard += ("\n" + player + " Final Four wins: " + "\n" + str(rd5_wins) + "\n\n")

        rd6_wins = []
        for game in master_dictionary[player]:
            if game == 'total':
                continue
            else:
                if (master_dictionary[player][game][5] == 1):
                    rd3_wins.append(game)
        scoreboard += ("\n" + player + " Final Four wins: " + "\n" + str(rd6_wins) + "\n\n")

    msg = {'content': scoreboard}
    print(scoreboard)
    
    #requests.post(discord_url, headers = auth, data = msg)

    for player in master_dictionary:
        master_dictionary[player]['total']=0

def run_periodically(interval, function):
    next_time = time.time() + interval
    while True: 
        time.sleep(max(0, next_time - time.time()))
        try:
            function()
        except Exception:
            traceback.print_exc()

        time.sleep(interval)

main()
run_periodically(3600, main)







