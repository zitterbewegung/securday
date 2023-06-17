from flask import Flask, request                                                
from twilio.twiml.messaging_response import MessagingResponse                   
from inference import query_agent                                               
from redis import Redis                                                         
from rq import Queue                                                            
from msg import send_text_message                                               
import os, time, socket, sys, ipaddress                                         
from collections import deque                                                   
from typing import Dict, List, Optional, Any                                    
                                                                                
# All Context / API managers                                                    
app = Flask(__name__)                                                           
#celery_app = celery_init_app(app)                                              
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
                                                                                
    print("Inb_msg {}".format(inb_msg))                                         
    print("Req To phone number {}".format(to_phone_number))                     
    print("Req from phone number {}".format(from_phone_number))                 
    #result = handle_received_sms.delay(inb_msg, from_phone_number, to_phone_nu\
mber)                                                                           
    # Call function to process the SMS (e.g. process_sms) using Celery          
    #process_sms.apply_async(args=[message_body])                               
                                                                                
    #with Connection(redis.from_url(redis://localhost:6379/0)):                 
    #    q = Queue()                                                            
    #    task =                                                                 
    q.enqueue(send_text_message,                                                
              to_phone_number,                                                  
              from_phone_number,                                                
              inb_msg)                                                          
                                                                                
    response = "Test" #agent_chain.run(input=inb_msg)                           
    #response  = query_agent(inb_msg)                                           
                                                                                
    """Respond to incoming calls with a simple text message."""                 
    # Start our TwiML response                                                  
    # time.sleep(2)                                                             
    resp = MessagingResponse()                                                  
    # Add a message                                                             
    for msg in split_string(response):                                          
        resp.message(msg)                                                       
    #print(response)                                                            
                                                                                
    return str(resp)                                                            
                                                                                
                                                                                
if __name__ == "__main__":                                                      
    app.run(debug=True)  
