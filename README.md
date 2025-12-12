# FactRadar: Misinformation Detection System

**MisinfoGuard v2.1 🛡️**

AI-powered **Community Notes-style fact checker** using **multi-AI verification** with distributed tracing and memory management. This project was developed for the Mumbai Hacks hackathon.

## 🌟 Features

- **Multi-AI Consensus** - Gemini + Llama verify claims together
- **Claim Verification** - Check specific claims or headlines
- **TRUE/FALSE/MISLEADING Verdicts** - Clear, actionable results
- **Credible Sources** - Links to high-quality fact-checking sites
- **Community Notes Style** - Concise, neutral explanations
- **Memory Bank** - SQLite-based caching for instant repeated queries
- **Full Observability** - Structured logging, distributed tracing, and metrics

## 🏗️ Architecture

```
User Input (Claim/URL)
        ↓
CoordinatorAgent
├── EvidenceGathererAgent (parallel web searches with credibility scoring)
├── MultiAIFactChecker
│   ├── Gemini 2.0 Flash
│   └── Llama 3.3 70B (via Groq)
├── ExplainerAgent (Community Notes-style output)
└── MemoryBank (caching)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google Gemini API key (free)
- Groq API key (optional, free)

### Backend Setup

Navigate to the backend directory:

```bash
cd MisinfoGuard/Backend

# Create virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# (See .env.example for reference)
echo "GOOGLE_API_KEY=your_gemini_key_here" > .env
echo "GROQ_API_KEY=your_groq_key_here" >> .env

# Start backend
uvicorn app:app --reload
```

The backend API server will start on port `8000`.

### Frontend Setup

Navigate to the frontend directory:

```bash
cd MisinfoGuard/Frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend application will start on port `5173`.

## 📡 API Endpoints

### Main Verification
```http
POST /analyze
{
  "claim": "Vaccines cause autism",
  "url": "https://example.com/article" (optional)
}
```

**Response:**
```json
{
  "analysis": {
    "claim": "Vaccines cause autism",
    "final_verdict": "FALSE",
    "confidence": 0.98,
    "explanation": "This claim has been thoroughly debunked...",
    "ai_verdicts": [
      {
        "model_name": "Gemini 2.0 Flash",
        "verdict": "FALSE",
        "confidence": 0.99,
        "reasoning": "..."
      },
      {
        "model_name": "Llama 3.3 70B",
        "verdict": "FALSE",
        "confidence": 0.97,
        "reasoning": "..."
      }
    ],
    "sources": [...]
  }
}
```

### Monitoring
- `GET /health` - Agent health status
- `GET /metrics` - Performance metrics
- `GET /memory/stats` - Cache statistics

## 📁 Project Structure

```
FactRadar/
├── MisinfoGuard/
│   ├── Backend/
│   │   ├── app.py              # FastAPI application
│   │   ├── src/
│   │   │   ├── agents/         # Multi-agent orchestration
│   │   │   ├── memory/         # SQLite caching
│   │   │   ├── observability/  # Logging & Tracing
│   │   │   ├── core/           # Data models
│   │   │   └── tools/          # Search tools
│   │   ├── requirements.txt
│   │   └── .env
│   ├── Frontend/
│   │   ├── src/                # React application
│   │   ├── package.json
│   │   └── vite.config.ts
│   ├── memory_bank.db          # Persistence
│   └── users.db
└── README.md
```

## 🛠️ Technologies

**Backend:**
- FastAPI
- Google Gemini AI
- Llama 3.3 (Groq)
- SQLite
- DuckDuckGo Search

**Frontend:**
- React (TypeScript)
- Vite
- Tailwind CSS
- ReactMarkdown

## 📝 License

MIT

## 🤝 Contributing

This is a course submission project demonstrating multi-agent systems and observability patterns.
