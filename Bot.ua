loomis_backend_v1.py

from flask import Flask, request, jsonify from flask_cors import CORS import json import os

app = Flask(name) CORS(app)

DATA_FILE = 'users.json'

Load or initialize user data

def load_data(): if os.path.exists(DATA_FILE): with open(DATA_FILE, 'r') as f: return json.load(f) return {}

def save_data(data): with open(DATA_FILE, 'w') as f: json.dump(data, f, indent=2)

users = load_data()

Register or get user

@app.route('/api/register', methods=['POST']) def register(): user_id = request.json.get('user_id') if user_id not in users: users[user_id] = {"coins": 0, "clicks": 0, "upgrades": 0} save_data(users) return jsonify(users[user_id])

Click to earn coins

@app.route('/api/click', methods=['POST']) def click(): user_id = request.json.get('user_id') amount = 1 + users[user_id]['upgrades'] users[user_id]['coins'] += amount users[user_id]['clicks'] += 1 save_data(users) return jsonify({"coins": users[user_id]['coins']})

Get user stats

@app.route('/api/stats', methods=['GET']) def stats(): user_id = request.args.get('user_id') return jsonify(users.get(user_id, {}))

Buy upgrade

@app.route('/api/upgrade', methods=['POST']) def upgrade(): user_id = request.json.get('user_id') cost = 50 * (users[user_id]['upgrades'] + 1) if users[user_id]['coins'] >= cost: users[user_id]['coins'] -= cost users[user_id]['upgrades'] += 1 save_data(users) return jsonify({"success": True, "upgrades": users[user_id]['upgrades']}) return jsonify({"success": False, "error": "Not enough coins"})

if name == 'main': app.run(debug=True)

