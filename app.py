from flask import Flask, request, render_template, session, jsonify, send_file
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me'

OLLAMA_URL = 'http://127.0.0.1:11434/api/chat'
MODEL = 'mistral'


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


if __name__ == '__main__':
    app.run(debug=True)
