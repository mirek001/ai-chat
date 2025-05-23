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
