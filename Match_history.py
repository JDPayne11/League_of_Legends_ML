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
for i in range(5):
    temp = 'summoner' + str(i)
    player_info[temp] = Fc.Summoner(challenger_ladder['entries'][i]['summonerId'], 1660125600, 1660730400, challenger_ladder, api_key)
    print(i)
    time.sleep(8)    

print("Cooldown")
time.sleep(120)
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
print(total_games)

# games = {}
# for i, game in enumerate(total_games[0:2]):  
#     temp = 'Game' + str(i)
#     games[temp] = Fc.Match_details(game, api_key)
#     print(i)
#     time.sleep(130)

final_list = []

for game in total_games[0:2]:    

    game_details = Fc.Match_details(game, api_key)
    print(game_details)
    game_info = []
    game_info.append(game_details.Match_info['gameId'])
    game_info.append(game_details.Match_info['gameVersion'])
    game_info.append(game_details.Match_info['gameDuration'])
    
    Player_list = ['Player0', 'Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Player6', 'Player7', 'Player8', 'Player9']
    Players_stats = []
    Champion_stats = []
    
    for player in Player_list:
        Players = []
        
        Players.append(game_details.Match_info['gameId'])
        Players.append(game_details.player_position[player].summonerName)
        Players.append(game_details.player_position[player].wins)
        Players.append(game_details.player_position[player].losses)
        Players.append(game_details.player_position[player].Lane)
        Players.append(game_details.player_position[player].tier)
        Players.append(game_details.player_position[player].rank)
        Players.append(game_details.player_position[player].lp)
        Players.append(game_details.player_position[player].veteran)
        Players.append(game_details.player_position[player].winstreak)
        Players.append(game_details.player_position[player].summonerLevel)
        
        
        
        summonerSpell1 = str(game_details.player_position[player].summonerSpell1_id)
        summonerSpell2 = str(game_details.player_position[player].summonerSpell2_id)
        try:
            summonerSpell1 =  KeyMap_summoner_spells[summonerSpell1]
            Players.append(summonerSpell1)
        except:
            summonerSpell1 = 'NULL'
            Players.append(summonerSpell1)
        try:   
            summonerSpell2 =  KeyMap_summoner_spells[summonerSpell2]
            Players.append(summonerSpell2)
        except:
            summonerSpell2 = 'NULL'
            Players.append(summonerSpell2)
        
        
        champion_id = str(game_details.player_position[player].championid)
        try:
            champion = KeyMap_Champions[champion_id]
            Players.append(champion)
        except:
            champion = 'NULL'
            Players.append(champion)
        
        
        
        Players_stats.append(Players)
        
        Champion = []
        try:
            champion = KeyMap_Champions[champion_id]
            Champion.append(champion)
        except:
            Champion = 'NULL'
            Players.append(champion)
        Champion.append(game_details.player_position[player].kills)
        Champion.append(game_details.player_position[player].deaths)
        Champion.append(game_details.player_position[player].assists)
        Champion.append(game_details.player_position[player].player_win)  
        Champion.append(game_details.player_position[player].cs)
        Champion.append(game_details.player_position[player].pings)
        Champion.append(game_details.player_position[player].vision_score)      
        Champion_stats.append(Champion)

    
    
    
    
    Teams = []
    Teams.append(game_details.Match_info['gameId'])
    Teams.append(game_details.team1_win)
    for team in game_details.Match_info['teams']:
        Bans = []
        for ban in team['bans']:
            Current_ban = str(ban['championId'])
            try:
                Current_ban = KeyMap_Champions[Current_ban]
                Bans.append(Current_ban)
            except:
                Bans.append('NULL')

        Teams.append(Bans)

       
        
    final_list.append(game_info)
    final_list.append(Players_stats)
    final_list.append(Champion_stats)
    final_list.append(Teams)
    print(final_list)
    
    
    time.sleep(130)

    
for game_info in final_list:
    print(game_info)