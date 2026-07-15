 AI Chatbot - Technical Assessment

A responsive conversational AI chatbot built with Python and OpenAI, featuring a ChatGPT-style interface with context-aware responses and conversation history.

Features

- Conversational AI powered by OpenAI GPT models
- Responsive web interface for desktop and mobile devices
- Natural Language Processing with input validation and text normalization
- Context-aware responses with session-based conversation history
- RESTful API architecture with FastAPI for performance and scalability
- Session management with new chat and clear conversation support

Technology Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | FastAPI |
| AI Provider | OpenAI API |
| NLP Processing | Custom text processor with Unicode normalization |
| Frontend | HTML5, CSS3, JavaScript |
| Server | Uvicorn (ASGI) |
| Configuration | python-dotenv, Pydantic Settings |

Project Structure

```
ai-chatbot-assessment/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── nlp/
│   │   ├── memory.py
│   │   └── processor.py
│   ├── services/
│   │   └── chat_service.py
│   ├── config.py
│   ├── main.py
│   └── state.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── chat.js
├── templates/
│   └── index.html
├── .env.example
├── requirements.txt
└── run.py
```

Prerequisites

- Python 3.10 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

Installation

1. Clone or download this repository

2. Navigate to the project directory:
```
cd ai-chatbot-assessment
```

3. Create a virtual environment:
```
python -m venv venv
```

4. Activate the virtual environment:

Windows:
```
venv\Scripts\activate
```

macOS/Linux:
```
source venv/bin/activate
```

5. Install dependencies:
```
pip install -r requirements.txt
```

6. Configure environment variables:
```
copy .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key
```

 Running the Application

Start the server:
```
python run.py
```

Open your browser and visit:
```
http://localhost:8000
```

Alternative start command:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web chat interface |
| GET | `/api/health` | Health check and status |
| POST | `/api/session` | Create new chat session |
| POST | `/api/chat` | Send message and get AI response |
| GET | `/api/history/{session_id}` | Get conversation history |
| DELETE | `/api/session/{session_id}` | Clear conversation history |

 Example API Request

```
POST /api/chat
Content-Type: application/json

{
  "session_id": "your-session-id",
  "message": "Hello, how are you?"
}
```

 Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| OPENAI_API_KEY | - | Your OpenAI API key |
| OPENAI_MODEL | gpt-4o-mini | OpenAI model to use |
| MAX_HISTORY_MESSAGES | 20 | Max messages kept in context |
| MAX_TOKENS | 1024 | Max tokens per AI response |
| TEMPERATURE | 0.7 | Response creativity (0-1) |
| HOST | 0.0.0.0 | Server host |
| PORT | 8000 | Server port |

 Deployment

Deploy to any platform supporting Python ASGI apps:

- Render: Connect GitHub repo, set build command `pip install -r requirements.txt`, start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Railway: Deploy with Python runtime and set `OPENAI_API_KEY` in environment variables
- Heroku: Use Procfile with `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Set `OPENAI_API_KEY` as an environment variable in your deployment platform.

 Live Demo

Deploy the application using the steps above and share your deployment URL as the live demo link.

 Author

Technical Assessment Submission
