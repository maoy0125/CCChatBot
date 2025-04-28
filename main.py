from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
import requests
import os
import uuid
from datetime import datetime, timedelta
import random
import string
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())

# Set up session configuration - sessions expire after 1 day
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_KEY:
    raise ValueError('OPENAI_API_KEY environment variable missing!')
client = OpenAI(api_key=OPENAI_KEY)

# In-memory storage for chat sessions (in production, use a database)
chat_sessions = {}

# Clean up old sessions occasionally
last_cleanup = datetime.now()
CLEANUP_INTERVAL = timedelta(hours=24)

def get_location_name(latitude: float, longitude: float) -> str:
    """
    Disabled: This function is currently not available.
    """
    return ""

def get_nearby_halal_carts(latitude: float, longitude: float) -> List[Dict]:
    """
    Disabled: This function is currently not available.
    """
    return []

def simple_chatbot(user_input, chat_history):
    # Add system prompt at the start
    system_prompt = "You are a helpful assistant that specializes in Contemporary Civilization course in Columbia University. When a user inputs a question or statement into the chatbot, the system will respond in two parts: (1) a brief, accessible reply to the content of the query, and (2) a philosophical commentary delivered in the style and framework of one of five selected thinkers from the Contemporary Civilization syllabus — Immanuel Kant, Jeremy Bentham, G.W.F. Hegel, Karl Marx, or Friedrich Nietzsche. The bot may select the philosopher based on thematic relevance (e.g., a question on justice prompts a Kantian or Benthamite response), or randomly, depending on whether a clear link to one thinker exists. Always be friendly and concise."
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )
    response_content = response.choices[0].message.content
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response_content})
    return response_content

@app.route('/')
def index():
    # Generate a new session ID if one doesn't exist
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        # Initialize an empty chat session
        chat_sessions[session['session_id']] = {
            'history': [],
            'created_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat()
        }
    
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get or create session
    session_id = session.get('session_id')
    if not session_id or session_id not in chat_sessions:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        chat_sessions[session_id] = {
            'history': [],
            'created_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat()
        }
    
    # Get chat history for this session
    chat_history = chat_sessions[session_id]['history']
    
    # Update last activity timestamp
    chat_sessions[session_id]['last_activity'] = datetime.now().isoformat()
    
    # Get response from chatbot
    response = simple_chatbot(user_message, chat_history)
    
    # Store updated chat history
    chat_sessions[session_id]['history'] = chat_history
    
    # Clean up old sessions (optional - in a production app you'd do this in a background task)
    clean_old_sessions()
    
    return jsonify({'response': response})

@app.route('/get_history', methods=['GET'])
def get_history():
    session_id = session.get('session_id')
    if not session_id or session_id not in chat_sessions:
        return jsonify({'history': []})
    
    return jsonify({
        'history': chat_sessions[session_id]['history']
    })

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session_id = session.get('session_id')
    if session_id and session_id in chat_sessions:
        chat_sessions[session_id]['history'] = []
    
    return jsonify({'status': 'success'})

def clean_old_sessions():
    """Remove chat sessions that are older than 24 hours (to prevent memory leaks)"""
    now = datetime.now()
    sessions_to_remove = []
    
    for session_id, session_data in chat_sessions.items():
        # Parse the ISO format timestamp
        last_activity = datetime.fromisoformat(session_data['last_activity'])
        # Check if the session is older than 24 hours
        if (now - last_activity).total_seconds() > 86400:  # 24 hours in seconds
            sessions_to_remove.append(session_id)
    
    # Remove old sessions
    for session_id in sessions_to_remove:
        del chat_sessions[session_id]

if __name__ == '__main__':
    # Listen on all interfaces (0.0.0.0) and use port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
