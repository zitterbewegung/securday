import os, time, socket, sys, ipaddress, logging, json
from typing import Dict, List, Optional, Any
from collections import deque
import persistent_dictionary
from flask import Flask, request
import pika
from twilio.twiml.messaging_response import MessagingResponse

# All Context / API managers
app = Flask(__name__)

logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)

# def get_if_opt_out(phone_number):
#     with open('opt_out.csv', newline='') as csvfile:
#         opt_outreader = csv.reader(csvfile, delimiter=',', quotechar='"')
#         for row in opt_outreader:
#            if row[0] == phone_number and row[1] == "TRUE":
#                return True
#            else:
#                return False
# def set_opt_in(phone_number):
#     if not get_if_out(phone_number):
#         row_to_make = '"{}", "TRUE", "10", "2023-01-01 01:01:01.000", "2023-12-31 01:01:01.000"'

#         with open('opt_out.csv', 'w', newline='') as csvfile:
#             opt_outwriter = csv.writer(csvfile, delimiter=',',
#                             quotechar='"', quoting=csv.QUOTE_MINIMAL)
#             opt_out.writerow()


#def initialize_users()'"+13316255728", "TRUE", "10", "2023-01-01 01:01:01.000", "2023-12-31 01:01:01.000'
#'"+13316255728", "TRUE", "10", "2023-01-01 01:01:01.000", "2023-12-31 01:01:01.000"''"+13316255728", "TRUE", "10", "2023-01-01 01:01:01.000", "2023-12-31 01:01:01.000"'

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
    opt_out_filename = "opt_out_phonenumbers.json"

    inbound_request = {}
    inbound_request["inb_msg"] = inb_msg
    inbound_request["To"] = to_phone_number
    inbound_request["From"] = from_phone_number
    
    inbound_request_payload = str(json.dumps(inbound_request))


    with PersistentDict('opt_out.json', 'c', format='json') as opt_in:
        opt_in = d
        #with open(opt_out_filename) as json_file:
        #    opt_in = json.load(json_file)
 

        if opt_in.get(from_phone_number): 
            send_to_queue(inbound_request_payload)
        else:
            opt_in[from_phone_number] = True
    
        if "STOP" in inb_msg:
            opt_in[from_phone_number] = False

    #with open('opt_out_data.json', 'w') as outfile:
    #    json.dump(user, outfile)

    logging.info("Inb_msg {}".format(inb_msg))
    logging.info("Req To phone number {}".format(to_phone_number))
    logging.info("Req from phone number {}".format(from_phone_number))
  
    #Relaying back to twilio
    resp = MessagingResponse()
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
