# AI Chat

This is a simple Flask web application that connects to an Ollama server to provide an AI chat using the **mistral** model. The web page automatically refreshes the conversation every few seconds and sends messages without reloading the page.

## Requirements

- Python 3
- Flask
- requests

## Running

Use the provided `run.sh` script to set up a virtual environment, install dependencies and start the server:

```bash
./run.sh
```

By default the application expects an Ollama server running at `http://127.0.0.1:11434`.

## Desktop GUI

In addition to the web interface a simple desktop GUI is available. Once the
dependencies are installed you can run it with:

```bash
python3 gui.py
```

The GUI communicates with the same Ollama server and displays the conversation
in a scrollable window.

## Standalone Frontend Example

A very minimal HTML page that communicates directly with the Ollama API is included as `simple_frontend.html`. It is now also served by the Flask app at `/simple`, and a navigation menu links to it from the main chat page. You can open this file directly in your browser (no server required) or access it through the running Flask application. The page sends requests to `http://127.0.0.1:11434/api/chat` and displays the conversation locally.
