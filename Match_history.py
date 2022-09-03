import requests as re
import time
from Functions_Classes import Functions as Fc


api_key = Fc.getAPI_key()   

#Getting challenger Ladder
challenger_ladder = Fc.get_challenger_player_stats()     
player_info = {}
for i in range(len(challenger_ladder['entries'])):
    temp = 'summoner' + str(i)
    player_info[temp] = Fc.Summoner(challenger_ladder['entries'][i]['summonerId'], 1660125600, 1661335200)
    print(i)
    time.sleep(1)    

#Getting matches for each player listed on the challenger ladder
games = []
for key in player_info:
    games.append(player_info[key].matches)

#Joining together the sublists (games of each player)
total_games = []
for a in range(len(games)):
    for b in range (len(games[a])):
        total_games.append(games[a][b])

#Finding unique games
total_games = list(set(total_games))

games = {}
for i, game in enumerate(total_games):  
    temp = 'Game' + str(i)
    games[temp] = Fc.Match_details(game)
    print(i)
    time.sleep(30)

for game in games:            
    print(games.player_position['Player1'].Lane)