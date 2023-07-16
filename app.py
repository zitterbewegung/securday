import os, time, socket, sys, ipaddress, logging, json
from typing import Dict, List, Optional, Any
from collections import deque
from flask import Flask, request
import pika
from twilio.twiml.messaging_response import MessagingResponse

# All Context / API managers
app = Flask(__name__)

logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)

def split_string(input_string, max_length=320):
    strings_list = []
    input_string_length = len(input_string)

    for i in range(0, input_string_length, max_length):
        strings_list.append(input_string[i : i + max_length])

    return strings_list

def send_to_queue(inbound_request_payload):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue',
                          durable=True)

    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=inbound_request_payload,
                          properties=pika.BasicProperties(
                              delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    logging.info(" [x] Sent {}".format(inbound_request_payload))
    connection.close()

@app.route("/sms", methods=["POST"])
def chatgpt():
    """get incoming message"""
    inb_msg           = request.form["Body"]  # .lower()
    to_phone_number   = request.form["To"]
    from_phone_number = request.form["From"]

    inbound_request = {}
    inbound_request["inb_msg"] = inb_msg
    inbound_request["To"]      = to_phone_number
    inbound_request["From"]    = from_phone_number 

    inbound_request_payload = str(json.dumps(inbound_request))
    logging.info("Inbound Request Payload {}".format(inbound_request_payload))
    send_to_queue(inbound_request_payload)
    
    logging.info("Inb_msg {}".format(inb_msg))
    logging.info("Req To phone number {}".format(to_phone_number))
    logging.info("Req from phone number {}".format(from_phone_number))
  
    #Relaying back to twilio
    resp = MessagingResponse()
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
