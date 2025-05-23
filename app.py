from flask import Flask, request, render_template, session, jsonify

import requests

app = Flask(__name__)
app.secret_key = "change-me"

OLLAMA_API = "http://127.0.0.1:11434/api/chat"
MODEL_NAME = "mistral"


def query_ollama(history):
    payload = {
        "model": MODEL_NAME,
        "messages": history,
        "stream": False
    }
    response = requests.post(OLLAMA_API, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    message = data.get("message", {})
    return message.get("content", "")


@app.route('/', methods=['GET'])
def chat():
    if 'history' not in session:
        session['history'] = []
    return render_template('chat.html', history=session['history'])


@app.route('/api/messages', methods=['GET', 'POST'])
def messages():
    if 'history' not in session:
        session['history'] = []
    if request.method == 'POST':
        data = request.get_json() or {}
        text = data.get('message', '').strip()
        if text:
            session['history'].append({'role': 'user', 'content': text})

            try:
                reply = query_ollama(session['history'])
            except Exception as exc:
                reply = f"Error: {exc}"
            session['history'].append({'role': 'assistant', 'content': reply})
    return jsonify(history=session['history'])



if __name__ == '__main__':
    app.run(debug=True)
