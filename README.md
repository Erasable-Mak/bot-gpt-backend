# BOT GPT Backend

A Flask-based backend for the BOT GPT conversational AI platform.

## Features
- RESTful API for conversation management
- Integration with Groq API for LLM responses
- Simulated RAG functionality
- User and conversation persistence with SQLite
- Clean modular architecture

## Setup

```bash
1. Clone the repository:
git clone REPO_GIT_UTL
cd bot-gpt-backend

2. Create Python venv(poetry or venv):
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1

3. Install dependencies:
pip install -r requirements.txt

3. setup .env in /app folder, alternative .env variable values can be fetched from AWS Secrets as per ENV:
LLM_PROVIDER=groq
GROQ_API_KEY=YOUR_SECRET_API_KEY
GROQ_MODEL=llama-3.1-8b-instant
DATABASE_URL=sqlite:///botgpt.db

4. Run Application:
python run.py

5. Check application functioning:
a) Create a user

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/api/users" `
  -ContentType "application/json" `
  -Body '{"username":"mak3"}'

b) Create a document (for RAG)

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/api/documents" `
  -ContentType "application/json" `
  -Body '{"user_id":3,"title":"Sample PDF","uri":"s3://stub.pdf"}'

c) Create a conversation (open chat)

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/api/conversations" `
  -ContentType "application/json" `
  -Body '{"user_id":3,"message":"Hello"}'

d) Create a conversation (rag)

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/api/conversations" `
  -ContentType "application/json" `
  -Body '{"user_id":1,"message":"Summarize","mode":"rag","document_ids":["<doc_id>"]}'

e) Add a message
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/api/conversations/<conversation_id>/messages" `
  -ContentType "application/json" `
  -Body '{"message":"Next question"}'

f) List conversations
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:5000/api/users/3/conversations"

Remember User_id and field are subjected to change.


Note: Currently this project is using "@bp.route" which can be change to "connexion" "swagger/schema.yml" file that is already present and main file will be functional. 


IMPORTANT NOTICE: RUNS on python 3.11.9
