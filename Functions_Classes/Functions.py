# Functions
import requests as re
import time
from Functions_Classes import Functions as Fc
import json

def getAPI_key():
    
    ''' 
    Returns my api key from the previous folder
    '''
    
    with open("../api_key.txt", "r") as f:
    
        return f.read()


def check_status(api_key):    
    
    ''' 
    Returns the status of the riot API
    '''
    
    url = 'https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5'
    header_dict = {
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": api_key
    }
    
    return re.get(url, headers = header_dict).status_code

def KeyMap_Champions():
    
    #Matches key values of champions with their names, useful later in the script
    with open('data/champion_map.txt', 'r', encoding="utf8") as champList_file:
        champList = json.load(champList_file)
        champList_file.close()
        champList = champList['data']
    
    champNames = []
    champKeys = []
    for value in champList:
        champNames.append(value)
        champKeys.append(champList[value]['key'])
        
    mapped_champions = dict(zip(champKeys, champNames))    
    return mapped_champions


def KeyMap_summoner_spells():
    
    #Matches key values of champions with their names, useful later in the script
    with open('data/summoner_spell_map.txt', 'r', encoding="utf8") as summonerList_file:
        summonerList = json.load(summonerList_file)
        summonerList_file.close()
        summonerList = summonerList['data']
    
    SummonerNames = []
    SummonerKeys = []
    for value in summonerList:
        SummonerNames.append(value)
        SummonerKeys.append(summonerList[value]['key'])
        
    mapped_summoners = dict(zip(SummonerKeys, SummonerNames))    
    return mapped_summoners


def get_challenger_player_stats(api_key):
    
    ''' 
    This function calls the v4 API ranked_solo_5x5 endpoint
    Returns all players in challenger and includes stats such as win/loss, winstreak and rank information in json format
    '''
    
    url = 'https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5'
    header_dict = {
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": api_key
    }
   
    return re.get(url, headers = header_dict).json()


def get_challenger_player_id(player_id, api_key):
    
    ''' 
    Takes as input the player_id(encrypted summoner id) and returns a list of account information from the summoner-V4 api and encryptedAccountId endpoint
    Account information includes  puuid(needed to retrieve match information and summoner name and is returned in json format
    '''
  
    url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/' + player_id
    header_dict = {
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": api_key
    }
           
    return re.get(url, headers = header_dict).json()


def get_matches(puuid, startTime_Unix, endTime_Unix, api_key):
    
    ''' 
    Takes the puuid of a player as input as well as a start and end time in Unix to specify the range to retrieve games.
    The function calls the v5/matches api and uses the puuid endpoint to retrieve matches played
    Returns a list of matches played in the specified range
    '''
    
    url = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid + '/ids'
    header_dict = {
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": api_key
    }
    
    params_dict = {

        'startTime' : startTime_Unix,
        'endTime' : endTime_Unix,
        
        #Only picking ranked 5v5 games
        'queue' : 420,
        'type' : 'ranked',
        
        #Only grabbing the first 50 results
        'start' : 0,
        'count' : 50
    }
    return re.get(url, headers = header_dict, params = params_dict).json()


def get_match_info(match, api_key):
    
    ''' 
    Takes in a match id as input
    Retrieves all match details using the v5/matches Api and matchId endpoint
    Returns match details in json format
    '''
    
    url = 'https://americas.api.riotgames.com/lol/match/v5/matches/' + match
    header_dict = {
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": api_key
    }
    
    return re.get(url, headers = header_dict).json()


def get_player_stats(summoner_id, api_key):
    
    '''
    Takes in an encrypted summoner id as input
    Retrieves player information using the v4 api and uses the encrypted summoner id endpoint
    Returns player stats in json format
    '''
    
    url = 'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summoner_id
    header_dict = {
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": api_key
    }
    return re.get(url, headers = header_dict).json()


#Classes
class Summoner:
    
    ''' This class represents all information surrounding a challenger player.
    To intialize a summoner a valid Id is required as well as a start and end time in Unix to specifiy the range
    to retrieve games.
    
    Attributes include:
        .summonerId : players encrypted summoner Id
        .summonerName : Players display name in game
        .puuid : Players puuid
        .summonerLevel
    
    Methods include
        .accounts : Uses the get_challenger_player_id function to find account information on the specified player
        .matches : returns a list of matches the player has played
        .total_matches : Total matches played in the previously specified time range
    '''
    
    def __init__(self, summonerId, startTime_Unix, endTime_Unix, challenger_ladder, api_key):
        self.summonerId = summonerId
        
        #Looping through the ladder until a match is found with the input summoner id
        for value in challenger_ladder['entries']:
            if value['summonerId'] == self.summonerId:
                self.summonerName = value['summonerName']
        
        #Finds all the accounts of the player in dictionary format
        self.accounts = get_challenger_player_id(summonerId, api_key)
        #Finds the puuid of the player
        self.puuid = self.accounts['puuid']
        #Finds the players summoner level
        self.summonerLevel = self.accounts['summonerLevel']
        
        #Returns a list of matches the player has played based on the parameters in the get_matches function
        self.matches = get_matches(self.puuid, startTime_Unix, endTime_Unix, api_key)
        
        #Total games played by this summoner on this specific patch
        self.total_matches = len(self.matches)
        
        
class Match_details:
    
    '''
    This class represents all information surrounding a specified match.
    To intialize a Match_details class a Match_id is required.
    
    Attributes include:
        .Match_id
        .Match_info : all collected data from the game in json format
        .players : all collected data from each player in json format
        .team1 : Team 1 collected data such as bans, win/loss
        .team2 : Team 2 collected data such as bans, win/loss
        .team1_win 
        .team2_win 
        .team1_bans : Json format of team1 bans
        .team2_bans : Json format of team2 bans
        .summoner_Id : Retrives a list of summoner ids found in the game
        
    Methods include:
        .call : calls the match v5 api using the get_match_info function
        .player_position : Returns a dictionary of player information as it initializes 10 player classes which each call the matches V5 api once
        
    Sub_classes include:
        Player() : Holds information surrounding each player in the game such as their pick/lane and id. More info can be found inside.
        
        
    '''
    
    def __init__(self, Match_id, api_key):
        self.Match_id = Match_id
        print(self.Match_id)
        #Calling matchesV5 api
        self.call = get_match_info(Match_id, api_key)
        
        #Storing api call and filtering out uneeded data

        self.Match_info = self.call['info']

        
        #list of dictionaries including stats for each player
        self.players = self.Match_info['participants']
        
        #Tracking team information
        self.team1 = self.Match_info['teams'][0]
        self.team2 = self.Match_info['teams'][1]
        
        #Storing winning and losing team
        self.team1_win = self.team1['win']
        
        #Storing bans for each team
        self.team1_bans = self.team1['bans']
        self.team2_bans = self.team1['bans']
        
        #Creating a list of encrypted summoner ids
        self.summoner_Id = []
        for i, player in enumerate(self.players):
            self.summoner_Id.append(player['summonerId'])
            
        
        #Creating a player class to hold data on each player in the game
        class Player:
            
            '''
            This subclass represents each players stats in the current game.
            To initialize a player their encrypted summoner id is required as well as the self.players attribute from the Match_details class.
            
            Attributes:
                .summoner_Id
                .players : The players exhaustive list of stats within the game
                .Lane : The position the player played (top,jungle,mid,adc,supp)
                .championId : The champion the player played in integer format
                .teamId : The team the player was on
                
            Methods:
                .player_stats : Uses the get_player_stats function to get player information. Check the function docstring for a return value description            
            '''
    
            def __init__(self, summoner_Id, players, api_key):
                self.current_summoner_Id = summoner_Id
                print(self.current_summoner_Id)
                # Holds lane, champion and team of given player
                self.players = players
                for value in self.players:
                    if value['summonerId'] == self.current_summoner_Id:
                        
                        #Tracking player information
                        self.summonerName = value['summonerName']
                        self.Lane = value['individualPosition']
                        self.teamId = value['teamId']
                        self.summonerLevel = value['summonerLevel']
                        #Key mapping champion ids and summoner spells into names

                        
                        self.championid = str(value['championId'])
                        
                        
                        self.summonerSpell1_id = value['summoner1Id']
                        self.summonerSpell2_id = value['summoner2Id'] 
                        
                        
                            
                        #Getting in game stats (kills, deaths, assists, win, cs, pings, vision score)
                        self.kills = value['kills']
                        self.deaths = value['deaths']
                        self.assists = value['assists']
                        self.player_win = value['win']
                        self.cs = value['totalMinionsKilled']
                        self.pings = value['basicPings']
                        self.vision_score = value['visionScore']
                        
                        #Assigning team names
                        if self.teamId == 100:
                            self.teamId = 'team1'
                        elif self.teamId == 200:
                            self.teamId = 'team2'
                #Grabbing winrate/winstreak/rank/lp of the given player        
                self.player_stats = get_player_stats(self.current_summoner_Id, api_key)
                    
                for queue in self.player_stats:
                    try:
                        if queue['queueType'] == 'RANKED_SOLO_5x5':
                            self.wins = queue['wins']
                            self.losses = queue['losses']
                            self.tier = queue['tier']
                            self.rank = queue['rank']
                            self.lp = queue['leaguePoints']
                            self.veteran = queue['veteran']
                            self.winstreak = queue['hotStreak']

                    except:
                        self.wins = 'NULL'
                        self.losses = 'NULL'
                        self.tier = 'NULL'
                        self.rank = 'NULL'
                        self.lp = 'NULL'
                        self.veteran = 'NULL'
                        self.winstreak = 'NULL'
                        print('Error')
                        continue
                        
        
        #Creating a dictionary to hold all the player information (lane, champion, team)
        self.player_position = {}
        for i, summoner_Id in enumerate(self.summoner_Id):
            temp = 'Player' + str(i)
            self.player_position[temp] = Player(summoner_Id, self.players, api_key)
            time.sleep(18)
                
