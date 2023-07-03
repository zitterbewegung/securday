import os
import redis
import json

from twilio.rest import Client
from multiprocessing import Process

redis_conn = redis.Redis(charset="utf-8", decode_responses=True)


def sub(name: str):
    pubsub = redis_conn.pubsub()
    pubsub.subscribe("channel")
    for message in pubsub.listen():
        if message.get("type") == "message":
            data = json.loads(message.get("data"))
            print("%s : %s" % (name, data))

            account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
            auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

            body = data.get("message")
            from_ = data.get("from")
            to = data.get("to")
                                        
            message = client.messages.create(from_=from_, to=to, body=body)
            #conversation = client.conversations \
            #    .v1 \
            #                     .conversations \
            #                     .create(friendly_name='Saati conversation')

                                 
            print("message id: %s" % message.sid)



if __name__ == "__main__":
    Process(target=sub, args=("reader1",)).start()

    print("connection...")
