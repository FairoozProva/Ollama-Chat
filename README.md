# Local LLM Chat (Streamlit + Ollama)

A Streamlit web interface to chat with a locally hosted LLM running through Ollama.

## Features
- Chat input and response area with streaming output
- Conversation history panel
- Reset conversation button
- Model dropdown (fetched from Ollama's `/api/tags`)
- Temperature slider
- Download chat as a text file
- Error handling when Ollama is not running

## Tech stack
Python, Streamlit, Requests, Ollama

## Setup
1. Install Ollama from https://ollama.com
2. Pull a model:
```
   ollama pull llama3.2
```
3. Create and activate a virtual environment:
```
   python -m venv venv
   venv\Scripts\activate
```
4. Install dependencies:
```
   pip install -r requirements.txt
```
5. Run the app:
```
   streamlit run app.py
```
6. Open http://localhost:8501

## How it works
Streamlit (frontend) sends a POST request to Ollama's `/api/chat` endpoint
at `http://localhost:11434`. The full message history is sent each time so the
model remembers the conversation. Responses are streamed back chunk by chunk.

## Screenshots
![Chat](screenshots/chat.png)
![Sidebar](screenshots/sidebar.png)
![Error handling](screenshots/error-handling.png)
