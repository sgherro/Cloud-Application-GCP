import base64
import json
import os

from flask import Flask, render_template, request

project_id = 'esercizio1a'
topic_name = 'testTopic'

app = Flask(__name__)

app.config['PUBSUB_VERIFICATION_TOKEN'] = os.environ['PUBSUB_VERIFICATION_TOKEN']

MESSAGES = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', messages = MESSAGES)

@app.route('/pubsub/push', methods = ['POST'])
def pubsub_push():
    print("Received push")
    if request.args.get('token','') != app.config['PUBSUB_VERIFICATION_TOKEN']:
        return 'Invalid request', 404

    envelope = json.loads(request.data.decode('utf-8'))
    payload = base64.b64decode(envelope['message']['data'])
    MESSAGES.append(payload)
    print("ciao")
    return 'OK',200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug =True)