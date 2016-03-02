from flask import Flask, render_template, request, json
import json


app = Flask(__name__)

# list of team twitter handles back in 2010, which more closely aligns with the training data set sent over
# http://www.sportsgeekery.com/466/the-complete-list-of-official-nfl-team-twitter-accounts/
with open('listOf2010TeamTwitterHandles.json') as handlesFileOld:    
    oldTeamHandles = json.load(handlesFileOld)

# current list of nfl team twitter handles
# https://twitter.com/NFL/lists/nfl-teams/members?lang=en
with open('listOfCurrentNFLTwitterHandles.json') as handlesFile:    
    currentTeamHandles = json.load(handlesFile)

# dict where team names are the keys and city names are the values
with open('teamNames.json') as teamNamesFile:    
    teamNames = json.load(teamNamesFile)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submitMessage',methods=['POST','GET'])
def submitMessage():
    message = request.form['newMessage']



if __name__ == '__main__':
    app.run(debug=True)
    
