from transformers import HfAgent

from huggingface_hub import login
import os, time, yaml
from collections import deque
from typing import Dict, List, Optional, Any
from flask import Flask, request
from shodan import Shodan
from twilio.twiml.messaging_response import MessagingResponse

login("<YOUR_TOKEN>")

# Starcoder
agent = HfAgent("https://api-inference.huggingface.co/models/bigcode/starcoder")
# StarcoderBase
# agent = HfAgent("https://api-inference.huggingface.co/models/bigcode/starcoderbase")
# OpenAssistant
# agent = HfAgent(url_endpoint="https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5")

agent.chat("Show me an an image of a capybara")

from transformers import Tool
from huggingface_hub import list_models


class CatImageFetcher(Tool):
    name = "cat_fetcher"
    description = ("This is a tool that fetches an actual image of a cat online. It takes no input, and returns the image of a cat.")

    inputs = []
    outputs = ["text"]

    def __call__(self):
        return Image.open(requests.get('https://cataas.com/cat', stream=True).raw).resize((256, 256))

def subset_shodan(ip: str):
    api = Shodan(os.environ.get('SHODAN_API_KEY'))
    host = api.host(ip)
    return """
    IP: {}
    Organization: {}
    Operating System: {}
    Location: Lat {} Long {}
    Asn: {}
    Transport: {}
    """.format(host['ip_str'],
               host.get('org', 'n/a'),
               host.get('os', 'n/a'),
               host.get('lat', 'n/a'),
               host.get('long', 'n/a'),
               host.get('asn', 'n/a'),
               host.get('transport', 'n/a'))


@app.route("/endpoint", methods=["POST"])
def chatgpt():
    """get incoming message"""
    inb_msg           = request.form["Body"]  # .lower()
    print(inb_msg)

    response = agent.chat("Show me an an image of a capybara")

    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    # time.sleep(2)
    resp = MessagingResponse()
    # Add a message
    for msg in split_string(response):
        resp.message(msg)
    print(response)

    return str(resp)


if __name__ == "__main__":
    
    app.run(debug=True)


message = client.messages \
    .create(
         body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_='+15017122661',
         media_url=['https://c1.staticflickr.com/3/2899/14341091933_1e92e62d12_b.jpg'],
         to='+15558675310'
     )

print(message.sid)
