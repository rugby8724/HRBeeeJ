from flask import Flask, request, jsonify
import slack
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env' # Path to .env file
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
client.chat_postMessage(channel='#test-hack', text='Happy Hacking!')

app = Flask(__name__)

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    if data.get('type') == 'url_verification':
        return jsonify({'challenge': data.get('challenge')})
    
    if data.get('type') == 'event_callback':
        event = data.get('event')
        if event.get('type') == 'message':
            text = event.get('text')
            if text == 'hello':
                return jsonify({'text': 'world'})
            else:
                print('Message:', text)
        
    return '', 200
  
if __name__ == '__main__':
    app.run(port=3000)