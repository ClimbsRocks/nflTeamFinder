from flask import Flask, render_template, request, json
import json
from os import path


app = Flask(__name__)

# list of team twitter handles back in 2010, which more closely aligns with the training data
# http://www.sportsgeekery.com/466/the-complete-list-of-official-nfl-team-twitter-accounts/
with open( path.join('wordLists', 'listOf2010TeamTwitterHandles.json') ) as handlesFileOld:    
    oldTeamHandles = json.load(handlesFileOld)['teams']

# current list of nfl team twitter handles
# https://twitter.com/NFL/lists/nfl-teams/members?lang=en
with open( path.join('wordLists', 'listOfCurrentNFLTwitterHandles.json') ) as handlesFile:    
    currentTeamHandles = json.load(handlesFile)['teams']

# dict where team names are the keys and city names are the values
with open( path.join('wordLists', 'teamNames.json') ) as teamNamesFile:    
    teamNames = json.load(teamNamesFile)

# nicknames for each team from:
# https://foreshock.wordpress.com/origin-of-nfl-teams-1922-present/nfl-team-nicknames-goodbadoldnew/
with open( path.join('wordLists', 'teamNicknames.json') ) as teamNicknames:    
    teamNicknames = json.load(teamNicknames)['nicknames']

# list of footabll words taken from http://football.about.com/od/football101/a/Football-Glossary.htm
with open( path.join('wordLists', 'footballWords.json') ) as footballWordsFile:    
    footballWords = json.load(footballWordsFile)['words']

extendedFootballWords = footballWords + teamNames.values()

# render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

# handle the logic for determining if a message is about an NFL team or not
# 5 means it is highly likely the message is about an NFL team
# 1 means the message is probably not about an NFL team
@app.route('/submitMessage',methods=['POST','GET'])
def submitMessage():
    message = request.form['newMessage'].lower()

    # replace any possessive endings the user may have added
    message = message.replace("'s",'')
    message = message.replace("'",'')

    # try to find any of the team twitter handles in the message
    for handle in oldTeamHandles + currentTeamHandles:
        try:
            message.index('@' + handle.lower())
            return '5'
        except:
            pass

    # try to find each team name in the message
    for team in teamNames:
        try: 
            message.index(team.lower())
            # If we find both the team name and a city that an NFL team plays in
            # contained in the message, we're very certain this is about an NFL team.
            # Similarly, if we find any of our "football words" in addition to 
            # a team name, this message is very likely to be about an NFL team.
            # Lastly, if we find a team name and a team nickname, that is a
            # strong positive signal.
            for word in extendedFootballWords + teamNicknames:
                try:
                    message.index(word.lower())
                    return '5'
                except:
                    pass

            # If we find only the team name but not any other football words, 
            # we are only slightly confident this is about an NFL team.
            return '3'
        except:
            pass

    # If we weren't able to find any of the team names, look for team nicknames.
    # We have lower confidence in these nicknames, so we give them a lower score.
    for nickname in teamNicknames:
        try:
            message.index(nickname.lower())

            for word in extendedFootballWords:
                try:
                    message.index(word.lower())
                    # if we find a nickname and other football words
                    return '4'
                except:
                    pass

            # if we find a nickname, but no other football words
            return '2'
        except:
            pass


    # If we don't find either an official team name or any of the popular nicknames, 
    # return a low confidence that this message is about an NFL team.
    return '1'


if __name__ == '__main__':
    app.run()
    
