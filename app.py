from flask import Flask, request, render_template, session, jsonify, send_file
import requests
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me'

OLLAMA_URL = 'http://127.0.0.1:11434/api/chat'
MODEL = 'mistral'
DB_PATH = 'chat_history.db'


def init_db():
    """Ensure that the SQLite database and table exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT)'
    )
    conn.commit()
    conn.close()


def get_history():
    """Return the full conversation history from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT role, content FROM messages ORDER BY id')
    rows = c.fetchall()
    conn.close()
    return [{'role': r, 'content': m} for r, m in rows]


def add_message(role, content):
    """Insert a single message into the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO messages (role, content) VALUES (?, ?)', (role, content))
    conn.commit()
    conn.close()


def call_ollama(messages):
    payload = {
        'model': MODEL,
        'messages': messages,
        'stream': False
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data.get('message', {}).get('content', '')


@app.route('/')
def index():
    if 'history' not in session:
        session['history'] = []
    return render_template('index.html', history=session['history'])


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'history' not in session:
        session['history'] = []
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        text = data.get('message', '').strip()
        if text:
            session['history'].append({'role': 'user', 'content': text})
            try:
                reply = call_ollama(session['history'])
            except Exception as exc:
                reply = f'Error: {exc}'
            session['history'].append({'role': 'assistant', 'content': reply})
    return jsonify(history=session['history'])


@app.route('/simple')
def simple_frontend():
    """Serve the standalone simple frontend page."""
    return send_file('simple_frontend.html')


@app.route('/simple/history')
def simple_history():
    """Return conversation history stored in the database."""
    return jsonify(history=get_history())


@app.route('/simple/chat', methods=['POST'])
def simple_chat_api():
    """Handle chat messages for the simple frontend using persistent storage."""
    data = request.get_json(silent=True) or {}
    text = data.get('message', '').strip()
    if text:
        add_message('user', text)
        history = get_history()
        try:
            reply = call_ollama(history)
        except Exception as exc:
            reply = f'Error: {exc}'
        add_message('assistant', reply)
    return jsonify(history=get_history())


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
