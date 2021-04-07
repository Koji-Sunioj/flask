from __future__ import print_function
import datetime
import pickle
import pandas as pd
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def scopes():
	SCOPES = ['https://www.googleapis.com/auth/calendar']
	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('/home/kokogabriel/credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)
	return creds

def main(start,end=None,query='Ikea'):
	creds = scopes()
	service = build('calendar', 'v3', credentials=creds)
	events_result = service.events().list(calendarId='primary',timeMin=start,timeMax=end,singleEvents=True,orderBy='startTime',q=query).execute()
	events = events_result.get('items', [])
	
	if not events:
		print('No upcoming events found.')
	
	cal_id = [event['id'] for event in events]
	db_date = [pd.to_datetime(event['start']['dateTime']).strftime('%Y-%m-%d') for event in events]
	start_time = [pd.to_datetime(event['start']['dateTime'][:18]) for event in events]
	end_time = [pd.to_datetime(event['end']['dateTime'][:18]) for event in events]
	title = [event['summary'] for event in events]
    
	frame = pd.DataFrame(data= {'cal_id':cal_id,'start_time':start_time,'end_time':end_time,'title':title},index=pd.to_datetime(db_date))
	frame.index.name = 'db_date'
	frame['category'] = 'work'
	return frame

