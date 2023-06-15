from twilio.twiml.messaging_response import MessagingResponse
from inference import query_agent

def split_string(input_string, max_length=320):
    strings_list = []
    input_string_length = len(input_string)

    for i in range(0, input_string_length, max_length):
        strings_list.append(input_string[i:i + max_length])

    return strings_list


def handle_received_sms(message, to_phone_number, from_phone_number):
    # Do something with the message
    # ...
    # Send an SMS (this can also be a background task if needed)
    #inb_msg           =  request.form["Body"]  # .lower()
    #to_phone_number   = '+13316255728' #request.form["To"]
    #from_phone_number = '+17784035044' #request.form["From"]
    #breakpoint()
    result = query_agent(message)
    #breakpoint()
    send_sms(result, to_phone_number, from_phone_number)

def send_sms(message, to_phone_number, from_phone_number):
    from twilio.rest import Client
    # Replace with your Twilio account details
    account_sid = 'AC5bcff59dbca312a39f93ff9998a03f63'
    auth_token = 'ac33a22d951b391f41d82479e65fd999'
    
    client = Client(account_sid, auth_token)
    #resp = ""
    #for msg in split_string(response):
    #    resp.message(msg)
        
    # Replace 'to' with the recipient's phone number and 'from_' with your Twilio number
    client.messages.create(to=to_phone_number, from_=from_phone_number, body=message)
