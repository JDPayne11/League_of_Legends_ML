import requests as re
import time
from Functions_Classes import Functions as Fc
import json

#Getting API key and initializing functions
api_key = Fc.getAPI_key()   
print(api_key)
KeyMap_Champions = Fc.KeyMap_Champions()
KeyMap_summoner_spells = Fc.KeyMap_summoner_spells()
#Grabbing entire challenger ladder
challenger_ladder = Fc.get_challenger_player_stats(api_key)   
player_info = {}

#Retrieving players from challenger in range(x). The summoner object calls the api for match history and stores it
for i in range(300):
    temp = 'summoner' + str(i)
    player_info[temp] = Fc.Summoner(challenger_ladder['entries'][i]['summonerId'], 1660125600, 1660730400, challenger_ladder, api_key)
    print(i)                        #Printing current player
    print(player_info[temp])        #Printing the stored player object
    time.sleep(2)                   #Resting to not overcall API

#Checkpoint
print(player_info)
print("Cooldown")
time.sleep(120)    #Resetting calling timer before next step


#Getting matches for each player listed on the challenger ladder
games = []
for key in player_info:
    games.append(player_info[key].matches)   #Retrieving .matches stored in the current Summoner object

#Joining together the sublists (games of each player)
total_games = []
for a in range(len(games)):
    for b in range (len(games[a])):
        total_games.append(games[a][b])

#Finding unique games
total_games = list(set(total_games))

#Retrieving all important information for a match
for game in total_games:    
    print(total_games.index(game))
    
    #Calls the API for us and returns to us a bunch of attributes that we can call for

    game_details = Fc.Match_details(game, api_key)
    
    print(game_details)
    print("Current Game of " + str(len(total_games)))
    print(total_games.index(game))
    
    #Stores game_id, game_version, and game_duration
    game_info = []
    game_info.append(game_details.Match_info['gameId'])
    game_info.append(game_details.Match_info['gameVersion'])
    game_info.append(game_details.Match_info['gameDuration'])
    
    Player_list = ['Player0', 'Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Player6', 'Player7', 'Player8', 'Player9']
    
    #Stores every players overall stats
    Players_stats = []
    
    #Stores every players stats within the specific game
    Champion_stats = []
    
    for player in Player_list:
        
        #Stores the current players overall stats
        Players = []
        
        #Stores the current players stats within the current game
        Champion = []
        
        #Storing game ID
        Players.append(game_details.Match_info['gameId'])
        
        
        try:
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
            champion_id = str(game_details.player_position[player].championid)
        except Exception as e:       
            Players.append('NULL')
            Players.append('NULL')
            Players.append('NULL')
            Players.append('NULL')
            Players.append('NULL')
            Players.append('NULL')
            Players.append('NULL')
            Players.append('NULL')
            Players.append('NULL')
            Players.append('NULL')
            print(e)
            continue
        
        try:
            summonerSpell1 =  KeyMap_summoner_spells[summonerSpell1]
            Players.append(summonerSpell1)
        except Exception as e:
            summonerSpell1 = 'NULL'
            Players.append(summonerSpell1)
            print(e)
            continue
        
        
        try:   
            summonerSpell2 =  KeyMap_summoner_spells[summonerSpell2]
            Players.append(summonerSpell2)
        except Exception as e:
            summonerSpell2 = 'NULL'
            Players.append(summonerSpell2)
            print(e)
            continue
        

        try:
            champion = KeyMap_Champions[champion_id]
            Players.append(champion)
        except Exception as e:
            Champion = 'NULL'
            Players.append(champion)
            print(e)
            continue
        
        Players_stats.append(Players)
        
            
            
        Champion.append(game_details.Match_info['gameId'])
        try:
            champion = KeyMap_Champions[champion_id]
            Champion.append(champion)
        except Exception as e:
            Champion = 'NULL'
            Players.append(champion)
            print(e)
            continue
        
        
        try:    
            Champion.append(game_details.player_position[player].kills)
            Champion.append(game_details.player_position[player].deaths)
            Champion.append(game_details.player_position[player].assists)
            Champion.append(game_details.player_position[player].player_win)  
            Champion.append(game_details.player_position[player].cs)
            Champion.append(game_details.player_position[player].pings)
            Champion.append(game_details.player_position[player].vision_score)
        except Exception as e:
            Champion.append('NULL')
            Champion.append('NULL')
            Champion.append('NULL')
            Champion.append('NULL')
            Champion.append('NULL')
            Champion.append('NULL')
            Champion.append('NULL')
            Players.append(champion)
            print(e)
            continue
            
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

    import csv  
    with open('data/Games.csv', 'a', encoding="utf-8") as f:
        thewriter = csv.writer(f)
        thewriter.writerow(game_info)

    with open('data/Players.csv', 'a', encoding="utf-8") as f:
        thewriter = csv.writer(f)
        thewriter.writerow(Players_stats)

        
    with open('data/Champion_stats.csv', 'a', encoding="utf-8") as f:
        thewriter = csv.writer(f)
        thewriter.writerow(Champion_stats)
        
    with open('data/Teams.csv', 'a', encoding="utf-8") as f:
        thewriter = csv.writer(f)
        thewriter.writerow(Teams)

    
    print('Game Finished')
    time.sleep(18)
        

    
