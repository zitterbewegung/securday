import os
from dotenv import load_dotenv
import requests
from inference import query_agent
from twilio.rest import Client
load_dotenv()

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN= os.environ.get('TWILIO_AUTH_TOKEN')

client = Client()

def send_text_message(from_, to, body):
    result = query_agent(message)
    client.messages.create(from_=from_, to=to, body=processed)

