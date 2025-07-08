from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Mongo setup (example)
client = MongoClient('mongodb://localhost:27017/')
db = client['webhookDB']
collection = db['events']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def get_events():
    events = list(collection.find({}, {'_id': 0}))  # exclude _id from results
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)