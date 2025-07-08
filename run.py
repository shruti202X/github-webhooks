from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['webhookDB']
collection = db['events']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def get_events():
    events = list(collection.find({}, {'_id': 0}))
    return jsonify(events)

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json

    # Identify the event type from headers
    event_type = request.headers.get('X-GitHub-Event')
    author = ""
    from_branch = ""
    to_branch = ""
    timestamp = ""

    if event_type == "push":
        author = payload['pusher']['name']
        to_branch = payload['ref'].split('/')[-1]
        timestamp = payload['head_commit']['timestamp']

    elif event_type == "pull_request":
        action = payload['action']
        if action in ["opened", "synchronize"]:
            author = payload['pull_request']['user']['login']
            from_branch = payload['pull_request']['head']['ref']
            to_branch = payload['pull_request']['base']['ref']
            timestamp = payload['pull_request']['created_at']

    elif event_type == "merge":
        # GitHub does not send a separate "merge" event.
        # Merges are tracked via push or pull_request merged status.
        pass

    else:
        return jsonify({"status": "ignored event"}), 200

    # Insert into MongoDB
    event_doc = {
        "author": author,
        "action_type": event_type,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": timestamp
    }

    collection.insert_one(event_doc)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)
