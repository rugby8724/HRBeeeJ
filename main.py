from flask import Flask, request, jsonify

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