from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
import pprint
import json

load_dotenv()
app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
CORS(app)

db = client.fish_db

def to_json(data):
    return jsonify(json.loads(json.dumps(data, default=str)))

@app.route('/api', methods=['POST'])
def new_post():
    post = request.get_json()
    ret = db.posts.insert_one(post)
    return to_json({
      'message': 'new post added',
      'acknowledged': ret.acknowledged,
      'inserted_id': ret.inserted_id
      })

@app.route('/api', methods=['GET'])
def get_posts():
    ret = []
    for post in db.posts.find():
        ret += [post]
    return to_json(ret)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()