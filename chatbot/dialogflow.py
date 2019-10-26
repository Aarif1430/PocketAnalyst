'''Dialogflow backend client (is that confusing?) 

This will all be structured as follows:

dialogflow.py is the 'client' interface that the backend uses to pass messages to the chatbot
The backend will be the interface between fb messenger, dialogflow, and our database that stores user info

In a sense, dialogflow handles the intent, while python code handles business logic + more complex responses


'''

import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
import random


from config import *

#setup
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

def send_msg_to_bot(message, session_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=message, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raisesession
    #process_response(response.query_result)
    return response.query_result

def process_response(df_response):
    for i in range(len(df_response.fulfillment_messages)):
        out_message = df_response.fulfillment_messages[i].text.text[0]
        #do something with the messages. Right now, I'll just print them
        print(out_message)

def handle_user_message(message, userid):
    user_registered = False #figure this out later
    session_id = hash(userid)
    resp = send_msg_to_bot(message, session_id)
    print(resp.intent.display_name)
    if(resp.intent.display_name in PROTECTED_INTENTS and not user_registered):
        print("oops! that intent is protected. try registering, then using it")
        #send something to user asking for them to register
    else:
        process_response(resp)

r = send_msg_to_bot("Hey, can I register?", 19291)

'''
SESSION_ID = 'current-user-id'
text_to_be_analyzed = "Hi! I'm David and I'd like to eat some sushi, can you help me?"
session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
query_input = dialogflow.types.QueryInput(text=text_input)
try:
    response = session_client.detect_intent(session=session, query_input=query_input)
except InvalidArgument:
    raisesession
'''