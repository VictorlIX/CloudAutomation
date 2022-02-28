import datetime
import logging

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    
    

    

    from vsts.vss_connection import VssConnection
    from msrest.authentication import BasicAuthentication
    import vsts.work.v4_1.models as models
    from vsts.work_item_tracking.v4_1.models.wiql import Wiql
    import base64 #need for encrypting the token
    from pprint import pprint
    import itertools
    import re
    import smtplib
    import os
    from datetime import date
    import datefinder
    import datetime
    from datetime import datetime
    from knack.util import CLIError
    from vstsclient.vstsclient import VstsClient
    import requests
    import json
    import jsonpatch
    from vstsclient.models import JsonPatchDocument, JsonPatchOperation
    from vstsclient.constants import SystemFields, MicrosoftFields
    import requests
    import base64
    
    
    # Fill in with your personal access token and org URL
    personal_access_token = 'PAT'
    
    
    encode_token = encodedBytes = base64.b64encode(':'.join(personal_access_token).encode("ascii"))
    
    organization_url = 'https://dev.azure.com/Org'
    
    
    # Create a connection to the org
    credentials = BasicAuthentication('', personal_access_token)
    connection = VssConnection(base_url=organization_url, creds=credentials)
    
    # Get a client (the "core" client provides access to projects, teams, etc)
    core_client = connection.get_client('vsts.core.v4_0.core_client.CoreClient')
    
    # Get the list of projects in the org
    projects = core_client.get_projects()
    
    encode_token = encodedBytes = base64.b64encode(personal_access_token.encode("ascii"))
    
    # Project choice that the program will be looking inside and working with
    ##working_project = choice("Choose project:", projects, lambda project: project.name)
    working_project = projects[0]
    print(str(working_project))
    z=0
    
    
    
    
    teams = core_client.get_teams(project_id=working_project.id)
    
    #working_team = choice("Choose team:", teams, lambda team: team.name)
    working_team = teams[0]
    print(str(working_team))
    
    # Get work client for access to boards
    work_client = connection.get_client('vsts.work.v4_1.work_client.WorkClient')
    work_tracking_client = connection.get_client('vsts.work_item_tracking.v4_1.work_item_tracking_client.WorkItemTrackingClient')
    
    
    team_context = models.TeamContext(project_id=working_project.id, team_id=working_team.id)
    print(str(team_context))
    # Creates a query
    wiql_query = Wiql(
        query="SELECT [System.Title] FROM workitems WHERE [System.Title] CONTAINS WORDS 'Meeting' AND [System.State] IN ('Active', 'New') ORDER BY [System.CreatedDate] asc"
        )
    # Obtains work item information
    query_results = work_tracking_client.query_by_wiql(wiql_query, team_context=team_context)
    
    
    # start a list to parse the work items data into
    work_items = []
    # loop through each work itme
    a=0
    x=0
    b=0
    
    for x in query_results.work_items:
        a=a+1
        print("number of meeting work items: "+ str(a))
        #try/except block to catch keyerror message and continue
        try:
            y=work_tracking_client.get_work_item(x.id)
            #print(y)
        # break the azure devops data into simpler bits
            title = y.fields['System.Title']
            titlewithdate = str(title)
            print("Title: " + titlewithdate)
            matches = list(datefinder.find_dates(titlewithdate))
            if len(matches) > 0:
            # date returned will be a datetime.datetime object. here we are only using the first match.
                date = matches[0]
                print("Date created: " + str(date))
                
                now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                print("Todays date: " + str(now))
                diff = str(datetime.now() - date)
                number = "".join(diff)
                numtostring= re.findall('\d+', number)
                firstnum = int(numtostring[0])
                #print (re.findall('\d+', number ))
                print(str(firstnum) + " Day Difference" )
                
                
                if firstnum >= 5:
                    b=b+1
                    print("Higher than 5 days. Item will be closed.")
                    print("trying to close........")
                    authorization = str(base64.b64encode(bytes(':'+personal_access_token, 'ascii')), 'ascii')
                    headers = {
                    'Content-Type': 'application/json-patch+json', #specify the content-type
                    'Authorization': 'Basic '+authorization
                    } 
                    url="https://dev.azure.com/Org/Project_apis/wit/workitems/"+str(y.id)+"?api-version=6.0"
                    body = [{
                    "op": "add",
                    "path": "/fields/System.State",
                    "value": "Closed"
                    }]
                    response = requests.patch(url, json = body, headers=headers)
                    print(response.__dict__)
    
                    #work_tracking_client.Close(y.id)
                    print(str(y.id) + " was closed")
                    
                    
                    #print("ID " + str(y.id) + " Has been deleted")
                else: 
                    print("Number below 5 days. Will not be deleted")
                #print(number)
                
    
                
                
            else:
                print('No dates found') 
        
        
            user = y.fields['System.AssignedTo']
            #print(user)
            state = y.fields['System.State']
            #field = y.fields['System.ReferenceName']
            #print(str(field) + " This is the field")
            print(state)
            parts = user.split('<')
            #print(parts)
            name = parts[0].strip()
            #print(name)
            email = parts[1].strip('>')
            #print(email)
            priority = y.fields['Microsoft.VSTS.Common.Priority']
            #print(priority)
            idNum = str(y.id)
            print("ID: " +idNum)
            revNum = str(y.rev)
            print("REV: " +revNum)
            url = "https://dev.azure.com/Org/Project/_workitems/edit/" + idNum +"/"
    
            title = y.fields['System.Title']
            print()
            print()
                    
        except KeyError:
            continue
         
         
         
    if mytimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function ran at %s', utc_timestamp)        
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         

























