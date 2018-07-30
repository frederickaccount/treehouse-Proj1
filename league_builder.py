#Using Python 3.7.0
import csv

def read_soccer_players_csv():                                                           #Read CSV and place OrderedDict of players into a list
    with open("soccer_players.csv", newline='') as csvfile:
        player_reader = csv.DictReader(csvfile,delimiter = ',')
        rows = list(player_reader)
        return rows

def group_by_experience(players):                                                         #Place players in different lists depending on their Soccer Experience
    players_with_exp= []
    players_without_exp = []
    for player in players:
        if player['Soccer Experience'] == "YES":
            players_with_exp.append(({'Name' : player['Name'], 'Height (inches)': player['Height (inches)'],'Soccer Experience': player['Soccer Experience'], 'Guardian Name(s)': player['Guardian Name(s)']}))
        else:
            players_without_exp.append(({'Name' : player['Name'], 'Height (inches)': player['Height (inches)'],'Soccer Experience': player['Soccer Experience'], 'Guardian Name(s)': player['Guardian Name(s)']}))

    return (players_with_exp, players_without_exp)

def add_to_teams(players, sharks, raptors, dragons):                                      #Add first third of players to sharks, second to raptors, last to dragons
    count = 0
    for player in players:
        if count < (len(players)/3):
            sharks.append(({'Name' : player['Name'], 'Height (inches)': player['Height (inches)'],'Soccer Experience': player['Soccer Experience'], 'Guardian Name(s)': player['Guardian Name(s)']}))
        elif (count >= (len(players)/3) and count < (len(players) * 2/3)):
            raptors.append(({'Name' : player['Name'], ' Height (inches)': player['Height (inches)'],'Soccer Experience': player['Soccer Experience'], 'Guardian Name(s)': player['Guardian Name(s)']}))
        else:
            dragons.append(({'Name' : player['Name'], 'Height (inches)': player['Height (inches)'],'Soccer Experience': player['Soccer Experience'], 'Guardian Name(s)': player['Guardian Name(s)']}))
        count +=1

    return sharks, raptors, dragons

def prepare_team_message(team):                                                           #Prepare string for a teams player's info for teams.txt
    team_info = ""
    for player in team:
        team_info+= (", ".join((player['Name'], player['Soccer Experience'], player['Guardian Name(s)'])))
        team_info+= ("\n")
    return (team_info)

def make_teams_file(team1_info,team2_info,team3_info):                                    #Create teams.txt with team names, info for all players is passed in
    with open ("teams.txt", "w") as file:
        file.write("Sharks\n" + team1_info + "\nDragons \n" + team2_info + "\nRaptors \n" + team3_info)

def prepare_intro_letters(sharks,raptors,dragons):                                        #Combine all teams into one list, add team name and practice time to each dictionary
    all_players = []
    for player in sharks:
        all_players.append(({'Team':'Sharks', 'Name':player['Name'], 'Guardian Name(s)': player['Guardian Name(s)'], 'First Practice' : '8/30/2018 at 10:00 AM'}))
    for player in raptors:
        all_players.append(({'Team':'Raptors', 'Name':player['Name'], 'Guardian Name(s)': player['Guardian Name(s)'], 'First Practice' : '8/30/2018 at 10:00 AM'}))
    for player in dragons:
        all_players.append(({'Team':'Dragons', 'Name':player['Name'], 'Guardian Name(s)': player['Guardian Name(s)'], 'First Practice' : '8/30/2018 at 10:00 AM'}))
    return all_players

def make_letter_file(player_info):                                                        #create file names for each player name with _'s instead of spaces, lowercase. 
    for player in player_info:
        filename = ("{}.txt".format(player['Name'].replace(" ","_").lower()))
        with open (filename, "w") as file:
            file.write("Dear {}, \n{} has been drafted to the {}!\nFirst practice will begin on {}.".format(player['Guardian Name(s)'], player['Name'], player['Team'], player['First Practice'] ))

if __name__ == '__main__':                                                                  #Don't automatically run anything if this is being imported
    players = read_soccer_players_csv()                                                     #Get a list of dictionaries containing players from csv
    players_with_exp, players_without_exp=  group_by_experience(players)                    #divide list in two based on soccer experience
    sharks = []                                                                             #declare lists for each team
    raptors = []
    dragons = []
    if (len(players_with_exp) % 3 ==0 and len(players_without_exp) % 3 ==0):                #Check that players can be divided evenly into 3 teams
        sharks,raptors,dragons = add_to_teams(players_with_exp,sharks,raptors,dragons)      #Divide experienced players evenly and place them on teams
        sharks,raptors,dragons = add_to_teams(players_without_exp,sharks,raptors,dragons)   #Divide remaining players evenly and place them on teams
        sharks_info = prepare_team_message(sharks)                                          #Prepare strings to be placed in teams.txt for all teams  with names, soccer experience, and guardian names
        dragons_info = prepare_team_message(dragons)
        raptors_info = prepare_team_message(raptors)
        make_teams_file(sharks_info,dragons_info,raptors_info)                              #create teams.txt
        invitation_info = prepare_intro_letters(sharks,raptors,dragons)                     #prepare list of dictionaries with player info and add team names and practice times for each player
        make_letter_file(invitation_info)                                                   #create text files to serve as letters to the guardians of the players
