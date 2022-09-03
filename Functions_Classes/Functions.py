# Functions
def getAPI_key():
    
    ''' 
    Returns my api key from the previous folder
    '''
    
    f = open("../api_key.txt", "r")
    
    return f.read()


def check_status():    
    
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
        
    mapped_champions = dict(zip(champNames,champKeys))    
    return mapped_champions


def get_challenger_player_stats():
    
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


def get_challenger_player_id(player_id):
    
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


def get_matches(puuid, startTime_Unix, endTime_Unix):
    
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


def get_match_info(match):
    
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


def get_player_stats(summoner_id):
    
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
        .leaguepoints : Lp the player currently has
        .wins 
        .losses
        .hotstreak : If the player is on a winstreak
        .summonerName : Players display name in game
        .puuid : Players puuid
        .summonerLevel
    
    Methods include
        .accounts : Uses the get_challenger_player_id function to find account information on the specified player
        .matches : returns a list of matches the player has played
        .total_matches : Total matches played in the previously specified time range
    '''
    
    def __init__(self, summonerId, startTime_Unix, endTime_Unix):
        self.summonerId = summonerId
        
        #Looping through the ladder until a match is found with the input summoner id
        for value in challenger_ladder['entries']:
            if value['summonerId'] == self.summonerId:
                
                #Once correct player is found assign lp, wins, losses, winstreak, and ign to the player
                self.leaguepoints = value['leaguePoints']
                self.wins = value['wins']
                self.losses = value['losses']
                self.hotStreak = value['hotStreak']
                self.summonerName = value['summonerName']
        
        #Finds all the accounts of the player in dictionary format
        self.accounts = get_challenger_player_id(summonerId)
        #Finds the puuid of the player
        self.puuid = self.accounts['puuid']
        #Finds the players summoner level
        self.summonerLevel = self.accounts['summonerLevel']
        
        #Returns a list of matches the player has played based on the parameters in the get_matches function
        self.matches = get_matches(self.puuid, startTime_Unix, endTime_Unix)
        
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
    
    def __init__(self, Match_id):
        self.Match_id = Match_id
        
        #Calling matchesV5 api
        self.call = get_match_info(Match_id)
        
        #Storing api call and filtering out uneeded data
        self.Match_info = self.call['info']
        
        #list of dictionaries including stats for each player
        self.players = self.Match_info['participants']
        
        #Tracking team information
        self.team1 = self.Match_info['teams'][0]
        self.team2 = self.Match_info['teams'][1]
        
        #Storing winning and losing team
        self.team1_win = self.team1['win']
        self.team2_win = self.team2['win']
        
        #Storing bans for each team
        self.team2_bans = self.team1['bans']
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
    
            def __init__(self, summoner_Id, players):
                self.summoner_Id = summoner_Id
                # Holds lane, champion and team of given player
                self.players = players
                for value in self.players:
                    if value['summonerId'] == self.summoner_Id:
                        self.Lane = value['individualPosition']
                        self.championId = value['championId'] 
                        self.teamId = value['teamId']
                        if self.teamId == 100:
                            self.teamId = 'team1'
                        elif self.teamId == 200:
                            self.teamId = 'team2'
                #Grabbing winrate/winstreak/rank/lp of the given player        
                self.player_stats = get_player_stats(self.summoner_Id)

                        
        
        #Creating a dictionary to hold all the player information (lane, champion, team)
        self.player_position = {}
        for i, summoner_Id in enumerate(self.summoner_Id):
            temp = 'Player' + str(i)
            self.player_position[temp] = Player(summoner_Id, self.players)
                
