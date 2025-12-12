from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid
from datetime import datetime

from src.core.models import AnalysisRequest, AnalysisResponse
from src.agents.coordinator import CoordinatorAgent
from src.observability.logger import get_logger, set_trace_id_for_all
from src.observability.tracer import get_tracer
from src.observability.metrics import get_metrics

logger = get_logger(__name__)
metrics = get_metrics()

app = FastAPI(
    title="MisinfoGuard v2 - Multi-Agent System",
    version="2.0.0",
    description="Advanced misinformation detection with multi-agent architecture"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize coordinator agent
coordinator = CoordinatorAgent()

@app.middleware("http")
async def add_trace_id(request, call_next):
    """Add trace ID to all requests"""
    trace_id = str(uuid.uuid4())[:8]
    set_trace_id_for_all(trace_id)
    get_tracer().start_trace(trace_id)
    
    response = await call_next(request)
    response.headers["X-Trace-ID"] = trace_id
    return response

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_claim(request: AnalysisRequest):
    """
    Multi-AI claim verification endpoint
    
    Demonstrates:
    - Multi-AI consensus (Gemini + Groq)
    - Claim verification (not topic analysis)
    - Credible source gathering
    - Community Notes-style output
    - Memory bank caching
    """
    start_time = time.time()
    claim = request.claim.strip()
    url = request.url
    
    logger.info(f"📥 Verification request", claim=claim, url=url)
    metrics.counter("analysis_requests_total").inc()
    
    try:
        # Execute multi-AI verification
        analysis = await coordinator.analyze(claim, url)
        
        processing_time = time.time() - start_time
        
        # Record metrics
        metrics.histogram("analysis_duration_seconds").observe(processing_time)
        metrics.counter("claims_analyzed_total").inc()
        
        # Check if from cache
        cached = analysis.cached
        if cached:
            metrics.counter("cache_hits_total").inc()
        
        logger.info(
            f"✅ Verification complete",
            claim=claim,
            verdict=analysis.final_verdict,
            duration_ms=round(processing_time * 1000, 2),
            cached=cached
        )
        
        return AnalysisResponse(
            analysis=analysis,
            processing_time=processing_time,
            cached=cached
        )
        
    except Exception as e:
        metrics.counter("analysis_errors_total").inc()
        logger.error(f"❌ Verification failed", claim=claim, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """API info"""
    return {
        "name": "MisinfoGuard v2 - Community Notes Style",
        "version": "2.1.0",
        "architecture": "Multi-AI Verification System",
        "features": [
            "Multi-AI consensus (Gemini + Groq)",
            "Claim verification (TRUE/FALSE/MISLEADING)",
            "Credible source gathering",
            "Community Notes-style explanations",
            "Memory bank caching",
            "Distributed tracing"
        ],
        "endpoints": {
            "analyze": "POST /analyze - Verify a claim",
            "health": "GET /health - Health check",
            "metrics": "GET /metrics - Performance metrics",
            "memory": "GET /memory/stats - Memory bank statistics"
        }
    }

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "agents": {
            "coordinator": "active",
            "evidence_gatherer": "active",
            "fact_checker": "active",
            "credibility_assessor": "active",
            "explainer": "active"
        }
    }

@app.get("/metrics")
async def get_metrics_endpoint():
    """Get performance metrics"""
    return metrics.get_metrics()

@app.get("/memory/stats")
async def get_memory_stats():
    """Get memory bank statistics"""
    return coordinator.memory_bank.get_stats()

# Auth
from fastapi import Header, Depends
from src.core.auth import UserManager, UserLogin, UserSignup, UserResponse, Token

user_manager = UserManager()

@app.post("/auth/signup", response_model=UserResponse)
async def signup(user: UserSignup):
    """Register a new user"""
    try:
        created_user = user_manager.create_user(user)
        return created_user
    except ValueError as e:
         raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(status_code=500, detail=f"Signup processing failed: {str(e)}")

@app.post("/auth/login", response_model=Token)
async def login(user: UserLogin):
    """Login and get access token"""
    authenticated_user = user_manager.authenticate_user(user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = user_manager.create_access_token(
        data={"sub": authenticated_user.email, "id": authenticated_user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=UserResponse)
async def read_users_me(authorization: str = Header(None)):
    """Get current user info"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
            
        email = user_manager.verify_token(token)
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
            
        user = user_manager.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        return UserResponse(
            id=user['id'],
            email=user['email'],
            name=user['name'],
            created_at=user['created_at']
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
