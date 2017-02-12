import requests
import json, csv
import datetime
import ConfigParser, os, sys

config = ConfigParser.ConfigParser()
config.read('trello.ini')

key = config.get('TRELLO', 'key')
token = config.get('TRELLO', 'token')
thelist = config.get('TRELLO', 'list')
startdatefield = config.get('CUSTOM', 'startdate')
durationfield = config.get('CUSTOM', 'duration')
tempoidfield = config.get('CUSTOM', 'tempoid')

def getCardsbyMember(member):
    url = "https://api.trello.com/1/members/%s" % (member)
    querystring = {"fields":"username,fullName",
    "cards":"open","card_fields":"name,idList",
    "key":key,
    "token":token}
    headers = {
    'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return data

def getTempoData(cardid):
    url = "https://api.trello.com/1/cards/%s/pluginData" % (cardid)
    querystring = {"key":key,
    "token":token}
    headers = {
    'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.text
    j_data = data[1:len(data)-1]
    if len(j_data) > 0:
        return json.loads(j_data)
    else:
        return "NULL"

def writeToCSV(tempoid,startdate,duration,description):
    data = [tempoid, startdate, duration, description]
    f = open(str(filedate)+'.csv','a')
    w = csv.writer(f)
    w.writerow(data)
    f.close()

def getCompleteCard(cards):
    completedcard = []
    for card in cards:
        # find the card if it save in ##Completed
        if card["idList"] == thelist:
            cardname = card["name"]
            # get the custom field
            tempo_d = getTempoData(card["id"])
            # if there are TEMPO data
            if tempo_d != "NULL":
                d = json.loads(tempo_d["value"])
                startdate = d["fields"][startdatefield]
                duration = int(d["fields"][durationfield])*60*60
                tempoid = d["fields"][tempoidfield]
                myDict = {"tempoid": tempoid, "startdate": startdate, "duration": duration, "cardname":cardname}
                completedcard.append(myDict)
    return completedcard

filedate = datetime.date.today()
member = "539010c187655c291d15ef13"
d=getCardsbyMember(member)
cards=getCompleteCard(cards=d["cards"])
for card in cards:
    writeToCSV(card["tempoid"],card["startdate"],card["duration"],card["cardname"])
