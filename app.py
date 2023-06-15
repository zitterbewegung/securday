from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from inference import query_agent
from redis import Redis
from rq import Queue
from sms import handle_received_sms

import os, time, socket, sys, ipaddress
from collections import deque
from typing import Dict, List, Optional, Any
# from agent import BabyAG

# All Context / API managers
app = Flask(__name__)

# Set up RQ
redis_conn = Redis()
q = Queue(connection=redis_conn)

def split_string(input_string, max_length=320):
    strings_list = []
    input_string_length = len(input_string)

    for i in range(0, input_string_length, max_length):
        strings_list.append(input_string[i:i + max_length])

    return strings_list

@app.route("/sms", methods=["POST"])
def chatgpt():
    """get incoming message"""
    inb_msg           = request.form["Body"]  # .lower()
    to_phone_number   = request.form["To"]
    from_phone_number = request.form["From"]
    
    print(inb_msg)
    print(to_phone_number)
    print(from_phone_number)
    q.enqueue(handle_received_sms,
              inb_msg,
              from_phone_number,
              to_phone_number,)  

    #response = "Test" #agent_chain.run(input=inb_msg)
    #response  = query_agent(inb_msg)
    
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    # time.sleep(2)
    resp = MessagingResponse()
    # Add a message
    #for msg in split_string(response):
    #    resp.message(msg)
    #print(response)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
