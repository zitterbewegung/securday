import os
import redis
import sys
import json

redis_conn = redis.Redis(charset="utf-8", decode_responses=True)


def pub():
    data = {
        "message": "hello",
        "from": os.environ.get("TWILIO_PHONE_NUMBER"),
        "to": "YOUR_NUMBER",
    }
    # conversation = client.conversations \
    #                             .v1 \
    #                             .conversations('CHXK') \
    #                             .fetch()
    redis_conn.publish("channel", json.dumps(data))
    return {}


if __name__ == "__main__":
    pub()
