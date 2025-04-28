import json
import urllib.parse
from agent import getmyagent

def lambda_handler(event, context):
    print(f"Received event: {event}")

    # Parse the form-encoded data from Twilio
    body = event.get('body')
    if body:
        params = urllib.parse.parse_qs(body)
        message_body = params.get('Body', [''])[0]
    else:
        message_body = "No message body received"

    response_message = getmyagent(message_body) 

    twilio_response = f"""<?xml version="1.0" encoding="UTF-8"?><Response><Message>{response_message}</Message></Response>"""

    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/xml'},
        'body': twilio_response
    }