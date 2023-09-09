import os, time, socket, sys, ipaddress, logging, json
from typing import Dict, List, Optional, Any, LiteralString
from collections import deque
from persistent_dictionary import PersistentDict
from flask import Flask, request, session
from waitress import serve
import pika
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

# All Context / API managers
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
client = Client()


logging.basicConfig(filename="app.log", encoding="utf-8", level=logging.DEBUG)


def split_string(input_string, max_length=320):
    strings_list = []
    input_string_length = len(input_string)

    for i in range(0, input_string_length, max_length):
        strings_list.append(input_string[i : i + max_length])

    return strings_list


def send_to_queue(inbound_request_payload):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="task_queue", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=inbound_request_payload,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )
    logging.info(" [x] Sent {}".format(inbound_request_payload))
    connection.close()

@app.route("/status", methods=["GET"])
def status():
    return "App is online"
@app.route("/sms", methods=["POST"])
def main():
    """get incoming message"""
    inb_msg = request.form["Body"]  # .lower()
    to_phone_number = request.form["To"]
    from_phone_number = request.form["From"]
    incoming_filename = "incoming_phonenumbers.json"

    inbound_request = {}
    inbound_request["inb_msg"] = inb_msg
    inbound_request["To"] = to_phone_number
    inbound_request["From"] = from_phone_number

    inbound_request_payload = str(json.dumps(inbound_request))

    send_to_queue(inbound_request_payload)

    with PersistentDict(incoming_filename, "c", format="json") as prev_req:
        if prev_req.get(from_phone_number):
            previous_data = prev_req[from_phone_number]
            prev_req[from_phone_number] = previous_data.append(inbound_request)
        else:
            # client.messages.create(from_=to_phone_number,
            #                       to=from_phone_number,
            #                       body='Welcome to saturday!')
            prev_req[from_phone_number] = [inbound_request]

    logging.info("Inb_msg {}".format(inb_msg))
    logging.info("Req To phone number {}".format(to_phone_number))
    logging.info("Req from phone number {}".format(from_phone_number))

    # Relaying back to twilio
    resp = MessagingResponse()
    return str(resp)


if __name__ == "__main__":
    serve(app, port=5000)
    logging.info("App started")
    print("App Started")
