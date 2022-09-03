import requests as re
import time
from Functions_Classes import Functions as Fc
import json

api_key = Fc.getAPI_key()   
KeyMap_Champions = Fc.KeyMap_Champions()
KeyMap_summoner_spells = Fc.KeyMap_summoner_spells()
#Getting challenger Ladder
challenger_ladder = Fc.get_challenger_player_stats(api_key)     
player_info = {}
for i in range(2):
    temp = 'summoner' + str(i)
    player_info[temp] = Fc.Summoner(challenger_ladder['entries'][i]['summonerId'], 1660125600, 1661335200, challenger_ladder, api_key)
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
for i, game in enumerate(total_games[0:2]):  
    temp = 'Game' + str(i)
    games[temp] = Fc.Match_details(game, api_key)
    print(i)
    time.sleep(5)

final_list = []

for game in games:    

    game_info = []
    game_info.append(games[game].Match_info['gameId'])
    game_info.append(games[game].Match_info['gameVersion'])
    
    Player_list = ['Player0', 'Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Player6', 'Player7', 'Player8', 'Player9']
    Player_detail_from_game = []
    
    for player in Player_list:
        Players = []
        Players.append(games[game].Match_info['gameId'])
        Players.append(games[game].player_position[player].summonerName)
        Players.append(games[game].player_position[player].wins)
        Players.append(games[game].player_position[player].losses)
        Players.append(games[game].player_position[player].Lane)
        Players.append(games[game].player_position[player].championId)
        Players.append(games[game].player_position[player].tier)
        Players.append(games[game].player_position[player].rank)
        Players.append(games[game].player_position[player].lp)
        Players.append(games[game].player_position[player].veteran)
        Players.append(games[game].player_position[player].winstreak)
        Players.append(games[game].player_position[player].summonerLevel)
        Player_detail_from_game.append(Players)
    
    Teams = []
    Teams.append(games[game].team1_win)
    Teams.append(games[game].team2_win)
        
    final_list.append(game_info)
    final_list.append(Player_detail_from_game)
    final_list.append(Teams)

    
for game_info in final_list:
    print(game_info)