
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Fix path — works both locally and on Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, 'serviceAccountKey.json')

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/areas')
def get_areas():
    try:
        docs = db.collection('areas').stream()
        areas = []
        for doc in docs:
            areas.append(doc.to_dict())
        return jsonify(areas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/summary')
def get_summary():
    try:
        docs = db.collection('areas').stream()
        high, medium, low = 0, 0, 0
        for doc in docs:
            d = doc.to_dict()
            if d['Risk_Zone'] == 'High Risk':
                high += 1
            elif d['Risk_Zone'] == 'Medium Risk':
                medium += 1
            else:
                low += 1
        return jsonify({
            'high': high,
            'medium': medium,
            'low': low,
            'total': high + medium + low
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
