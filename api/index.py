from flask import Flask, request, jsonify, send_from_directory
import os
import sys

# Add the parent directory to sys.path to import from main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functionality from main.py
from main import app as flask_app, client, get_location_name, get_nearby_halal_carts, simple_chatbot

app = flask_app

# Make sure templates are correctly found
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path == '':
        return send_from_directory('../templates', 'index.html')
    # Handle static files
    if path.startswith('static/'):
        return send_from_directory('../', path)
    return send_from_directory('../', path)

# This is needed for Vercel
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
