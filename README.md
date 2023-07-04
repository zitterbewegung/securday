# Saturday

An SMS autonomous agent that assists in information security tasks.

## Description

An SMS autonomous agent that assists in information security tasks. Under the hood it uses langchain (a way to augment LLMs) that currently uses an SMS / MMS / Phone interface (you send a text message and it will respond to your phone) that will allow for basic information retrieval tasks (google search, searching shodan, google places) and has the goal of doing complex offensive and defensive security tasks using anything from a dumb phone to a smartphone. It is preprogramed with tools that it can intelligently use to accomplish certain tasks such as performing a search on shodan given an IP address.


## Getting Started

### Dependencies

* Python 3.10
* A twilio acccount
* An OpenAI account
* ngrok / static IP address

### Installing

* After installing Python create a virtualenv
* pip install -r requirements.txt
* Run python app.py for the main app
* Miniagi change .env.example and put the relevant credentials.
* Run recieve.py to start a messsage queue for simple tasks
* Run miniagi/pentest.py for the message queue consumer for pentesting.

### Executing program

* Send your SMS texts to the Twilio Phone Number you have bought.
* If you are getting a 500 error check issues with the twilio console.

```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Zitterbewegung

Special thanks to miniagi working out pentesting.

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the Apache 2.0 License - see the LICENSE.md file for details

## Acknowledgments

I have used an  Miniagi with modifications so that it can be accessed through SMS. I have made it use a message queue and also to only do pentesting.
* [miniagi](https://github.com/muellerberndt/mini-agi)
