# MisinfoGuard v2.1 🛡️

AI-powered **Community Notes-style fact checker** using **multi-AI verification** with distributed tracing and memory management.

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

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=your_gemini_key_here" > .env
echo "GROQ_API_KEY=your_groq_key_here" >> .env

# Start backend
uvicorn app:app --reload
```

The backend API server will start on port 8000.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend application will start on port 5173.

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

## 🎓 Course Concepts Demonstrated

This project demonstrates 5+ advanced agentic AI concepts:

1. ✅ **Multi-Agent System** - Coordinator + specialized agents
2. ✅ **Parallel Agents** - Concurrent execution with asyncio
3. ✅ **Memory Bank** - Long-term persistence with SQLite
4. ✅ **Custom Tools** - Enhanced search with parallel queries
5. ✅ **Observability** - Logging, tracing, and metrics

## 📁 Project Structure

```
Capstone/
├── app.py                      # FastAPI application
├── src/
│   ├── agents/
│   │   └── coordinator.py      # Multi-agent orchestration
│   ├── memory/
│   │   └── memory_bank.py      # SQLite caching
│   ├── observability/
│   │   ├── logger.py           # Structured logging
│   │   ├── tracer.py           # Distributed tracing
│   │   └── metrics.py          # Metrics collection
│   ├── core/
│   │   └── models.py           # Pydantic models
│   └── tools/
│       └── search.py           # Search tool
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── components/
│           └── ClaimCard.jsx
└── memory_bank.db              # SQLite database
```

## 🧪 Testing

1. **Fresh Analysis**: Search for "Climate Change"
2. **Cache Test**: Search same topic again (< 100ms)
3. **Metrics**: Navigate to the `/metrics` endpoint on the backend server.
4. **Memory Stats**: Navigate to the `/memory/stats` endpoint on the backend server.

## 📊 Performance

| Metric | v1.0 | v2.0 | Improvement |
|--------|------|------|-------------|
| API calls/claim | 3 | 1 | 66% ↓ |
| Parallel ops | 0 | 2-3 | 2x faster |
| Cached response | N/A | <100ms | Instant |

## 🛠️ Technologies

**Backend:**
- FastAPI
- Google Gemini AI
- SQLite
- DuckDuckGo Search

**Frontend:**
- React
- Vite
- ReactMarkdown

## 📝 License

MIT

## 🤝 Contributing

This is a course submission project demonstrating multi-agent systems and observability patterns.
