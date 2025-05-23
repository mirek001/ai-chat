import tkinter as tk
from tkinter import scrolledtext
import requests

OLLAMA_API = "http://127.0.0.1:11434/api/chat"
MODEL_NAME = "mistral"

history = []


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


def update_chat():
    chat.configure(state="normal")
    chat.delete(1.0, tk.END)
    for msg in history:
        chat.insert(tk.END, f"{msg['role']}: {msg['content']}\n")
    chat.configure(state="disabled")
    chat.yview(tk.END)


def send_message(event=None):
    text = entry.get().strip()
    if not text:
        return
    entry.delete(0, tk.END)
    history.append({"role": "user", "content": text})
    update_chat()
    root.update()
    try:
        reply = query_ollama(history)
    except Exception as exc:
        reply = f"Error: {exc}"
    history.append({"role": "assistant", "content": reply})
    update_chat()


root = tk.Tk()
root.title("AI Chat GUI")

chat = scrolledtext.ScrolledText(root, state="disabled", width=80, height=20)
chat.pack(padx=10, pady=10)

frame = tk.Frame(root)
frame.pack(fill="x", padx=10, pady=(0, 10))

entry = tk.Entry(frame)
entry.pack(side="left", fill="x", expand=True)
entry.bind("<Return>", send_message)

send_btn = tk.Button(frame, text="Send", command=send_message)
send_btn.pack(side="left", padx=(5, 0))

entry.focus()

root.mainloop()
