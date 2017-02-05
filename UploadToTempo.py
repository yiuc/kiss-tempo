import requests
import json
import ConfigParser, os

# Reference
# http://docs.python-guide.org/en/latest/scenarios/json/
# http://tempo.io/doc/timesheets/api/rest/latest/#1799179586

config = ConfigParser.ConfigParser()
config.read('jira.ini')

siteid = config.get('DEFAULT', 'HOST')
Authorization = config.get('DEFAULT', 'Authorization')
myname = config.get('TEMPO', 'name')
ProjectId = config.getint('TEMPO', 'ProjectId')

# tlscode: TLS-X
# startedtime: YYYY-MM-ddT00:00:00.000+0000
# timespent: in seconds
def createNewWorkLog(tlscode,startedtime,timespent,comment):
    url = "https://%s/rest/tempo-timesheets/3/worklogs/" % (siteid)
    payload = {
        'timeSpentSeconds': timespent,
        'dateStarted': startedtime,
        'comment': comment,
        'issue': {
            'projectId': ProjectId,
            'key': tlscode,
            'remainingEstimateSeconds': 0
        },
        'author': {
            'self': 'https://'+siteid+'/rest/api/2/user?username='+myname,
            'name': myname,
            'displayName': myname,
            'avatar':'https://'+siteid+'/secure/useravatar?size=small&ownerId='+myname
        },
        'worklogAttributes': [],
        'workAttributeValues': []
    }
    headers = {
        'content-type': "application/json",'x-atlassian-token': "no-check",'user-agent': "KISS-TEMPO",'Authorization': Authorization,'origin': "https://"+siteid,'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    return response.status_code

print (createNewWorkLog("TLS-8","2017-02-06T15:00:00.000+0000",3600,"test"));
