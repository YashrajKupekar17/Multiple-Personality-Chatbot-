# Multiple Personality Chatbot 🤖🎭

The **Multiple Personality Chatbot** is a modular, LangGraph-powered chatbot system that can dynamically switch between distinct AI personas during live conversations.

* **Factory Method Design** → A `CharacterFactory` generates unique personas with their own behaviors, tone, and quirks.
* **Seamless Personality Switching** → Users can interact with different personalities in real time, without restarting the chatbot.
* **Full-Stack Setup** → Backend (FastAPI) + Frontend (Streamlit) + MongoDB Atlas, all wired together with Docker.

---

## 📂 Project Structure

```
.
├── chatbot-api/            # Backend Service (FastAPI + LangGraph logic)
│   ├── src
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── .env.example
│   └── .env   (ignored locally)
│
├── chatbot-ui/             # Frontend Service (Streamlit UI)
│   ├── app.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── uv.lock
│   └── README.md
│
├── main.py                 # Entry point for local testing
├── docker-compose.yml      # Runs API + UI together
└── README.md               # You’re reading this 🙂
```

---

## 🏃 Quick Start (Docker Compose)

1. **Clone the repository**

   ```bash
   git clone <your_repo_url>
   cd multiple-personality-chatbot
   ```

2. **Configure environment variables**

   * Go to the API folder:

     ```bash
     cd chatbot-api
     cp .env.example .env
     ```
   * Open `.env` and set your **API keys** and **MongoDB Atlas connection URI**.

3. **Return to the root folder**

   ```bash
   cd ..
   ```

4. **Run with Docker Compose**

   ```bash
   docker compose up --build -d
   ```

   * UI → **[http://localhost:8501](http://localhost:8501)**
   * API → **[http://localhost:8000](http://localhost:8000)**

5. **Stop services**

   ```bash
   docker compose down
   ```

✅ You’re all set! Your chatbot is live with multiple personalities.

---

## 🗄 Environment Variables

Inside `chatbot-api/.env.example`:

```env
OPENAI_API_KEY="your_openai_key"

MONGO_URI="your_mongo_atlas_uri"
MONGO_DB_NAME=PersonalityChatbot
MONGO_COLLECTION=conversations

LANGSMITH_TRACING="true"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="your_langsmith_api_key"
LANGSMITH_PROJECT="MultiPersonaChatbot"
```

**Key fields explained:**

* **OPENAI_API_KEY** → Required for LLM calls.
* **MONGO_URI** → MongoDB Atlas connection string.
* **MONGO_DB_NAME / MONGO_COLLECTION** → Storage for chatbot states.
* **LANGSMITH*** → Optional LangSmith tracing & debugging support.

---

## 🛠 Development with LangGraph Studio

You can develop/test the chatbot personas directly in [LangGraph Studio](https://www.langchain.com/langgraph):

```bash
cd chatbot-api
langgraph dev --allow-blocking
```

---

## ⚙ Manual Setup (No Docker)

### Backend API

```bash
cd chatbot-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend UI

```bash
cd chatbot-ui
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

---

## 🐳 How Docker Works Here

* **API container** → FastAPI + LangGraph (port `8000`)
* **UI container** → Streamlit frontend (port `8501`)
* Both containers share a Docker network and talk via REST.
* MongoDB Atlas is external (not containerized).

---

## 🔄 Commands Recap

| Action                | Command                                                            |
| --------------------- | ------------------------------------------------------------------ |
| Start Docker services | `docker compose up --build -d`                                     |
| Stop Docker services  | `docker compose down`                                              |
| Run API manually      | `uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload`          |
| Run UI manually       | `streamlit run app.py --server.address 0.0.0.0 --server.port 8501` |
| Run LangGraph Studio  | `langgraph dev --allow-blocking`                                   |

---

## 🎭 Why Multiple Personas?

This chatbot isn’t just a single voice—it’s an ensemble cast. Thanks to the Factory Method, new personalities can be added by simply defining new `Character` classes. Each personality has its own speaking style, quirks, and behavioral logic, making conversations more engaging and flexible.

---
