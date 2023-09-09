#!/usr/bin/env python
import pika, sys, os, logging, re
from dotenv import load_dotenv
import json
import requests
from inference import agent_chain
from inference import query_agent
from twilio.rest import Client
load_dotenv()
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)


def main():

    client = Client()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue',
                          durable=True)

    def send_text_message(from_, to, body):
        '''
        Performs inference and then sends the text message.
        '''
        try:
            result = agent_chain.run(input=body)
        except ValueError:
            result = 'Sorry an error has occured please try again'
        logging.info(" [x] Sent %r" % body)
        client.messages.create(from_=from_, to=to, body=result)

    def callback(ch, method, properties, body):
        inbound_payload = json.loads(body)
        inb_msg = inbound_payload["inb_msg"]
        to_phone_number = inbound_payload["To"]     
        from_phone_number = inbound_payload["From"]
        send_text_message(to_phone_number, from_phone_number, inb_msg)
        logging.info(" [x] Received %r" % body)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue',
                          on_message_callback=callback,
                          auto_ack=True)
    logging.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
