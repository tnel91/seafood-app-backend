from flask import Flask, jsonify, request, render_template, Response
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

@app.route('/api', methods=['POST'])
def new_post():
    try:
        post = request.get_json()
        ret = db.posts.insert_one(post)
        return jsonify({
          'message': 'new post added',
          'acknowledged': ret.acknowledged,
          'inserted_id': str(ret.inserted_id)
          })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api', methods=['GET'])
def get_posts():
    try:
        res = db.posts.find({}, {'_id': False}).limit(100)
        return jsonify(list(res))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()