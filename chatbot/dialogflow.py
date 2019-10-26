'''Dialogflow backend client (is that confusing?) 

This will all be structured as follows:

dialogflow.py is the 'client' interface that the backend uses to pass messages to the chatbot
The backend will be the interface between fb messenger, dialogflow, and our database that stores user info

In a sense, dialogflow handles the intent, while python code handles business logic + more complex responses

TODO: ask docusign people to help meeeeee
'''
from config import *
#setup
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
import random

from pyshorteners import Shortener
shortener = Shortener('Tinyurl')


from docusign import *
from datastore import *


from image import main
from tickers import nameToTicker



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
    messages = []
    for i in range(len(df_response.fulfillment_messages)):
        out_message = df_response.fulfillment_messages[i].text.text[0]
        messages.append(out_message)
    return messages

def handle_user_message(message, userid):
    user_registered = True #figure this out later
    session_id = hash(userid)
    resp = send_msg_to_bot(message, session_id) #response.query_result
    print(resp.intent.display_name)
    if "account.create.q3" in resp.intent.display_name:
        #register user
        newuser = register_user(resp, userid)
        name = newuser["name"]
        riskmsg = "It seems you're a bit averse to risk -- totally ok! I'll keep that in mind when suggesting trades"
        if newuser["riskTolerance"]:
            riskmsg = "It seems that you're open to a bit of risk. I'll try to suggest trades that maximize your upside :)"
        doc_url = embedded_signing_ceremony()
        return ["Registration success. Welcome, " + name + ". Glad to have you on board!", riskmsg, "We're opened up a brokerage account for you at XYZbrokerage. Please make sure to sign this docusign form: " + shortener.short(doc_url)]
    elif resp.intent.display_name == "get-stock-info":
        company = resp.parameters.fields["company"].string_value.lower()
        print("displaying stock info")
        company = nameToTicker(company)
        main.generate_stock_info_image(company)
        msg = ["See for yourself ;)", "Here you go!", "Check it out:"][random.randint(0,2)]
        return [msg, {"path": "pil_text_font.png"}] #dicts are processed as images
    elif(resp.intent.display_name in PROTECTED_INTENTS and not user_registered):
        return ["Oops, you must be onboarded to do that! Ask me to sign up :)"]
    else:
        return process_response(resp)

def register_user(message_qr, userid):
    contexts = message_qr.output_contexts
    for i in range(len(contexts)):
        context = contexts[i]
        print(context)
        if(context.lifespan_count == 69):
            #this is the outputcontext
            userObj = {"id": userid}
            userObj["answer1"] = (context.parameters.fields["answer1"].string_value == 'true') or False
            userObj["answer2"] = not (context.parameters.fields["answer2"].string_value == 'true') or False #cause this is negative
            userObj["answer3"] = (context.parameters.fields["answer3"].string_value == 'true') or False
            userObj["name"] = dict(context.parameters)["person"].fields["name"].string_value
            riskScore = 0
            if(userObj["answer1"]):
                riskScore += 1
            if(userObj["answer2"]):
                riskScore += 1
            if(userObj["answer3"]):
                riskScore += 1
            newUser = {"id": userid, "name": userObj["name"], "riskTolerant": False}
            if riskScore >= 2:
                newUser["riskTolerance"] = True
            createUser(newUser)
            return newUser
    print("ayy")

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