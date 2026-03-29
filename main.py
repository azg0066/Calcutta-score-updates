import requests
import json
import time 
import traceback
import datetime
from datetime import date
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
import os


'''URLs from henrygd that pulls JSON scoreboard for a given day and returns as a JSON'''

url1 = "http://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2026/03/19"
url2 = "http://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2026/03/20"
url3 = "http://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2026/03/21"
url4 = "http://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2026/03/22"
url5 = "http://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2026/03/26"
url6 = "http://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2026/03/27"
url7 = "http://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2026/03/28"
url8 = "http://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2026/03/29"
url9 = "http://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2026/04/04"
url10 = "http://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/2026/04/06"

SEND_TO_DISCORD = False  # Set to True to enable Discord posting

RD2_START_DATE = date(2026,3,21)
RD3_START_DATE = date(2026,3,26)
RD4_START_DATE = date(2026,3,28)
RD5_START_DATE = date(2026,4,4)
RD6_START_DATE = date(2026,4,6)


WIL_INVESTMENT = 330
WES_INVESTMENT = 265
CHASE_INVESTMENT = 305

# Partial ownership from trades: {team: {player: fraction}}
TEAM_OWNERSHIP = {
    'Louisville':  {'Wes': 0.75, 'Chase': 0.25},
    'TCU':         {'Chase': 0.50, 'Wes': 0.50},
    'Texas':       {'Wes': 0.75, 'Chase': 0.25},
    'High Point':  {'Chase': 0.50, 'Wes': 0.50},
    'Arizona':     {'Wil': 0.95, 'Wes': 0.05},
    'Kansas':      {'Wil': 0.33, 'Wes': 0.67},
}




''' 
private discord information is saved in my .env file. the below accesses the variables in that file using the dotenv and os libraries.
'''
load_dotenv()
channel_id = os.getenv('DISCORD_CHANNEL_ID')
token = os.getenv('DISCORD_TOKEN')


discord_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
auth = {'authorization': f"Bot {token}"}


TOTAL_POT = 900

'''the below are cumulative win amounts; i.e., if a team wins 6 rounds, you just get RD6 winnings, not RD6 + RD5...'''

RD1_WIN = TOTAL_POT*0.005
RD2_WIN = TOTAL_POT*0.0175
RD3_WIN = TOTAL_POT*0.0525
RD4_WIN = TOTAL_POT*0.1025
RD5_WIN = TOTAL_POT*0.14
RD6_WIN = TOTAL_POT*0.205

'''contestant team lists -- should find a way to make this able to pull in directly from a CSV list'''

WIL_TEAMS = ['UCLA','South Florida', 'California Baptist', 'North Dakota St.', "Furman", "Siena", "Arizona", "Arkansas", "BYU", "Utah St.", "Missouri", "Michigan", "Kentucky", "Saint Louis", "Santa Clara", "Akron", "Hofstra", "Wright St.", "Tennessee St.", "Howard", "Florida", "Texas A&M", "VCU", "McNeese"]
WES_TEAMS = ['Michigan St.', 'Kansas', 'Louisville', 'Ohio St.', 'UCF', 'Gonzaga', 'Wisconsin', 'Miami (FL)', 'Villanova', 'Texas', 'Alabama', 'Tennessee', 'Houston', 'Nebraska', 'North Carolina', "St. Mary's (CA)", 'Iowa']
CHASE_TEAMS = ['Duke', 'UConn', "St. John's (NY)", 'TCU', 'UNI', 'Purdue', 'High Point', 'Hawaii', 'Kennesaw St.', 'Queens (NC)', 'LIU', 'Iowa St.', 'Virginia', 'Texas Tech', 'Georgia', 'Miami (OH)', 'Illinois', 'Vanderbilt', 'Clemson', 'Troy', 'Penn', 'Idaho', 'Prairie View']


master_dictionary = {'Wil':{'total': 0}, "Wes":{'total':0}, "Chase": {'total':0}}

'''
- creates a dictionary entry for each team in a contestant's team list, with a list of 0s corresponding to round wins
- thought about just using a single digit to indicate "latest round won", but the main thing is I want to be able to easily show a scoreboard with wins by round. TBD
'''
def setup():
    for team in WIL_TEAMS:
        master_dictionary['Wil'][team] = [0,0,0,0,0,0]
    for team in WES_TEAMS:
        master_dictionary['Wes'][team] = [0,0,0,0,0,0]
    for team in CHASE_TEAMS:
        master_dictionary['Chase'][team] = [0,0,0,0,0,0] 

'''
- takes each winner_round dictionary in the winner_list, searches through each player's list, and finds the player who owns the team. Then, updates that player's dictionary entry to reflect the dub.
- would like to think of a better name.  
'''
def update_player_wins(winner_list):
    for winner_round in winner_list:
        round = winner_round['round']
        winner = winner_round['winner']
        for player in master_dictionary:
            for team in master_dictionary[player]:
                if team == winner:
                    master_dictionary[player][team][round-1] =1


'''
- adds up winnings for each player and assigns the winnings to the "total" dictionary key. 
'''
def update_totals():
    win_amounts = [RD1_WIN, RD2_WIN, RD3_WIN, RD4_WIN, RD5_WIN, RD6_WIN]
    for player in master_dictionary:
        for team in master_dictionary[player]:
            if team == 'total':
                continue
            # Only pay the highest round won (cumulative, not additive)
            highest_round = -1
            for idx in range(5, -1, -1):
                if master_dictionary[player][team][idx] == 1:
                    highest_round = idx
                    break
            if highest_round >= 0:
                amount = win_amounts[highest_round]
                if team in TEAM_OWNERSHIP:
                    for owner, fraction in TEAM_OWNERSHIP[team].items():
                        master_dictionary[owner]['total'] += amount * fraction
                else:
                    master_dictionary[player]['total'] += amount


''' NO IDEA WHAT THIS WAS FOR. To be deleted.'''
def get_wins():
    rd1_wins = []
    rd2_wins = []
    rd3_wins = []
    for player in master_dictionary:
        if master_dictionary[player] == "total":
            continue
    

def main():
    setup() #creates the dictionary for each player. Why do this instead of just making these global variables at the beginning?
    
    # pulls game data list from each day.
    games_day1 = json.loads(requests.get(url=url1).content)["games"]
    games_day2 = json.loads(requests.get(url=url2).content)["games"]
    games_day3 = json.loads(requests.get(url=url3).content)["games"]
    games_day4 = json.loads(requests.get(url=url4).content)["games"]
    games_day5 = json.loads(requests.get(url=url5).content)["games"]
    games_day6 = json.loads(requests.get(url=url6).content)["games"]
    games_day7 = json.loads(requests.get(url=url7).content)["games"]
    games_day8 = json.loads(requests.get(url=url8).content)["games"]
    games_day9 = json.loads(requests.get(url=url9).content)["games"]
    games_day10 = json.loads(requests.get(url=url10).content)["games"]

    date_games = {
        date(2026,3,19): games_day1,
        date(2026,3,20): games_day2,
        date(2026,3,21): games_day3,
        date(2026,3,22): games_day4,
        date(2026,3,26): games_day5,
        date(2026,3,27): games_day6,
        date(2026,3,28): games_day7,
        date(2026,3,29): games_day8,
        date(2026,4,4):  games_day9,
        date(2026,4,6):  games_day10,
    }
    today_games = date_games.get(date.today(), [])

    winner_list = []
    
    '''checks the game data and adds winner_round dictionary entries to the winner_list.'''
    for game in games_day1:
        if not str(game['game']['bracketRound']).strip(): #not sure why I put this in.
            continue
        if (is_final(game)):
            result = get_winner(game)
            if result is not None:
                winner_list.append(result)
    for game in games_day2:
        if not str(game['game']['bracketRound']).strip():
            continue
        if (is_final(game)):
            result = get_winner(game)
            if result is not None:
                winner_list.append(result)
    for game in games_day3:
        if (is_final(game)):
            result = get_winner(game)
            if result is not None:
                winner_list.append(result)
    for game in games_day4:
        if not str(game['game']['bracketRound']).strip():
            continue
        if (is_final(game)):
            result = get_winner(game)
            if result is not None:
                winner_list.append(result)
    for game in games_day5:
        if not str(game['game']['bracketRound']).strip():
            continue
        if (is_final(game)):
            result = get_winner(game)
            if result is not None:
                winner_list.append(result)
    for game in games_day6:
        if not str(game['game']['bracketRound']).strip():
            continue
        if (is_final(game)):
            result = get_winner(game)
            if result is not None:
                winner_list.append(result)
    for game in games_day7:
        if not str(game['game']['bracketRound']).strip():
            continue
        if (is_final(game)):
            result = get_winner(game)
            if result is not None:
                winner_list.append(result)
    for game in games_day8:
        if not str(game['game']['bracketRound']).strip():
            continue
        if (is_final(game)):
            result = get_winner(game)
            if result is not None:
                winner_list.append(result)
    for game in games_day9:
        if not str(game['game']['bracketRound']).strip():
            continue
        if (is_final(game)):
            result = get_winner(game)
            if result is not None:
                winner_list.append(result)
    for game in games_day10:
        if not str(game['game']['bracketRound']).strip():
            continue
        if (is_final(game)):
            result = get_winner(game)
            if result is not None:
                winner_list.append(result)


    update_player_wins(winner_list=winner_list)
    update_totals()

    scoreboard = f'**🏀 SCOREBOARD** — {datetime.datetime.now(ZoneInfo("America/New_York")).strftime("%H:%M")} ET\n'
    scoreboard += '=' * 35 + '\n\n'

    # Leaderboard summary
    investments = {
        'Wil': WIL_INVESTMENT,
        'Wes': WES_INVESTMENT,
        'Chase': CHASE_INVESTMENT,
    }

    for player in master_dictionary:
        total = master_dictionary[player]['total']
        investment = investments.get(player, 0)
        roi = ((total - investment) / investment) * 100
        scoreboard += f'**{player}**: ${total:.2f} (ROI: {roi:+.1f}%)\n'

    scoreboard += '\n' + '-' * 35 + '\n'

    # Detailed wins per player
    rounds = [
        ('Round 1',      0, True),
        ('Round 2',      1, date.today() >= RD2_START_DATE),
        ('Sweet 16',     2, date.today() >= RD3_START_DATE),
        ('Elite 8',      3, date.today() >= RD4_START_DATE),
        ('Final 4',      4, date.today() >= RD5_START_DATE),
        ('Championship', 5, date.today() >= RD6_START_DATE),
    ]

    for player in master_dictionary:
        investment = investments.get(player, 0)
        total = master_dictionary[player]['total']
        roi = ((total - investment) / investment) * 100
        scoreboard += f'\n**{player}** — Total invested: ${investment} | ROI: {roi:+.1f}%\n'
        for round_name, idx, active in rounds: 
            if not active:
                break
            wins = []
            for g in master_dictionary[player]:
                if g != 'total' and master_dictionary[player][g][idx] == 1:
                    if g in TEAM_OWNERSHIP and player in TEAM_OWNERSHIP[g]:
                        pct = int(TEAM_OWNERSHIP[g][player] * 100)
                        wins.append(f'{g} ({pct}%)')
                    else:
                        wins.append(g)
            # Include partially owned teams from other players' rosters
            for team, owners in TEAM_OWNERSHIP.items():
                if player in owners and team not in master_dictionary[player]:
                    for other_player in master_dictionary:
                        if team in master_dictionary[other_player] and master_dictionary[other_player][team][idx] == 1:
                            pct = int(owners[player] * 100)
                            wins.append(f'{team} ({pct}%)')
                            break
            if wins:
                scoreboard += f'> {round_name}: {", ".join(wins)}\n'
        scoreboard += '\n'
        
    remaining = []
    for game in today_games:
        if not is_final(game):
            away = game['game']['away']['names']['short']
            home = game['game']['home']['names']['short']
            away_owner = get_owner(away)
            home_owner = get_owner(home)
            away_str = f"{away} ({away_owner})" if away_owner else away
            home_str = f"{home} ({home_owner})" if home_owner else home
            start_time = game['game'].get('startTime', 'TBD')
            remaining.append(f"{away_str} vs {home_str} — {start_time}")

    if remaining:
        scoreboard += '=' * 35 + '\n'
        scoreboard += '**Remaining Games Today**\n\n'
        for game_str in remaining:
            scoreboard += f'> {game_str}\n'
        scoreboard += '\n'

    scoreboard = scoreboard.rstrip('\n')
    msg = {'content': scoreboard}
    print(scoreboard)
    

    for player in master_dictionary:
        master_dictionary[player]['total']=0

    if SEND_TO_DISCORD:
        print(requests.post(discord_url, headers = auth, data = msg))


def get_owner(team):
    if team in TEAM_OWNERSHIP:
        parts = ', '.join(f'{p} {int(f*100)}%' for p, f in TEAM_OWNERSHIP[team].items())
        return parts
    if team in WIL_TEAMS:
        return 'Wil'
    if team in WES_TEAMS:
        return 'Wes'
    if team in CHASE_TEAMS:
        return 'Chase'
    return None


'''Checks if a game is complete.'''
def is_final(game):
    if game['game']['finalMessage']=='FINAL' or game['game']['finalMessage'] == 'FINAL (OT)':
        return True
    else:
        return False


'''Returns the winner and round of a completed game in the form of a dictionary.'''
def get_winner(game):
       
    bracketRound = str(game['game']['bracketRound']).strip()
    if not bracketRound.isdigit():
        return None
    round = int(bracketRound) - 1
    #for some reason, the "bracketRound" appears to be one higher than the actual in the raw data. E.g., for round one it says 2
    

    '''below lines determines if the away or home team won and assigns the winner to a local variable called "winner"'''
    if (game['game']['away']['winner']): 
        winner = game['game']['away']['names']['short']
    else:
        winner = game['game']['home']['names']['short']


    ''' creates final dictionary and assigns the round and winner.'''
    winner_round = {
        'round': round,
        'winner': winner
    }
    
    return winner_round


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
