# Saturday

An SMS autonomous agent that assists in information security tasks.

## Description

Under the hood it uses langchain (a way to augment LLMs) that currently uses an SMS / MMS / Phone interface (you send a text message and it will respond to your phone) that will allow for basic information retrieval tasks (google search, searching shodan, google places) and has the goal of doing complex offensive and defensive security tasks using anything from a dumb phone to a smartphone. It is preprogramed with tools that it can intelligently use to accomplish certain tasks such as performing a search on shodan given an IP address.


## Getting Started

### Dependencies

-  Software
   - Python 3.10+

   - Redis

   - Rabbitmq 
 
   #- Local operation curl ollama.ai/install.sh

-  Services
   - A twilio acccount
   - An OpenAI account
   - A shodan API Key
   - A wolfram alpha API key
   - ngrok / cloudflare / static IP address

### Installing & Execution

Create a virtualenv from requirements.py
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

I use ngrok to make a public ip that can be consumed from twilio
```
ngrok http 5000
```
Install rabbitmq using the script https://rabbitmq.com/install-debian.html

### Executing program


* Send your SMS texts to the Twilio Phone Number you have bought.
* If you are getting a 500 error check issues with the twilio console.

First start app.py
```
python app.py
```
Then start reciever.py

Then start receiver.py (at minium you need one of these).
```
python receiver.py

```


## Help

If you aren't seeing SMSs flowing down to the flask server look at the twilio console. You probably don't have the phone number URL / IP correctly entered.

Using ngrok for development or initial setup is recommended but not required. 
```
command to run if program contains helper info
```

## Authors

If you contribute to the project for your first contribution if you accept I will buy you gyros either through a gift card or in person depending on where you are.

ex. Zitterbewegung

Special thanks to miniagi working out pentesting.

## Version History

* 0.1
    * Initial Release
* 0.2
    * Added a web interface and added many tools. Reverse phone lookup to get information about a phone number, Virus total to see if a URL has a virus, censys to figure out if a location is an ip address and BashShell has been replaced with the new ShellTool in the latest version of langchain.

## License

This project is licensed under the Apache 2.0 License - see the LICENSE.md file for details

## Acknowledgments

I have used an  Miniagi with modifications so that it can be accessed through SMS. I have made it use a message queue and also to only do pentesting.
* [miniagi](https://github.com/muellerberndt/mini-agi)
