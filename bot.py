from flask import Flask, request, jsonify, Response
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env' # Path to .env file
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
# client.chat_postMessage(channel='#test-hack', text='Happy Hacking!')

BOT_ID = client.api_call("auth.test")['user_id']


@slack_event_adapter.on('message')
def message(payload):
    # print('Message:', payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    ts = event.get('ts')
    
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, thread_ts=ts, text=f'Hello {user_id}! you said: {text}')
        
@app.route('/hr-buzz', methods=['POST'])
def message_count():
    # event = payload.get('event', {})
    # print('Event:', event)
    data = request.form
    print('Data:', data)
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    text = data.get('text')

    client.chat_postMessage(channel=channel_id, text=f'User: {user_id} said: {text}')
    
    return Response('', status=200)


  
if __name__ == '__main__':
    app.run(debug=True, port=3000)