import os
import asyncio
import google.generativeai as genai
from typing import List, Optional, Dict
from datetime import datetime
import json
from dotenv import load_dotenv
from groq import Groq

from src.core.models import ClaimAnalysis, Evidence, AIVerdict
from src.memory.memory_bank import MemoryBank
from src.observability.logger import get_logger
from src.observability.tracer import trace_operation

load_dotenv()

logger = get_logger(__name__)

class BaseAgent:
    """Base class for all agents with common functionality"""
    
    def __init__(self, name: str):
        self.name = name
        logger.info(f"✅ Initialized {name}")
    
    async def execute(self, **kwargs):
        """Override in subclass"""
        raise NotImplementedError

class EvidenceGathererAgent(BaseAgent):
    """Specialized agent for gathering evidence from web sources"""
    
    def __init__(self):
        super().__init__("EvidenceGatherer")
        from src.tools.search import SearchTool
        self.search_tool = SearchTool()
    
    @trace_operation("evidence_gathering")
    async def gather(self, claim: str) -> List[Evidence]:
        """Gather evidence from multiple sources in parallel"""
        logger.info(f"🔎 Gathering evidence for claim: {claim}")
        
        # Search queries focused on crisis verification and official sources
        queries = [
            f"{claim} official statement",
            f"{claim} police verification",
            f"{claim} fact check india",
            f"{claim} government notification"
        ]
        
        # Execute searches in parallel
        tasks = [
            asyncio.to_thread(self.search_tool.search, query, max_results=3)
            for query in queries
        ]
        
        results_list = await asyncio.gather(*tasks)
        
        # Deduplicate and convert to Evidence
        all_evidence = []
        seen_urls = set()
        
        for results in results_list:
            for result in results:
                url = result.get('href')
                if not url or url in seen_urls:
                    continue
                
                # Filter out Chinese/Foreign domains if they leak through
                if url.endswith(('.cn', '.ru', '.xyz')) or 'zh-' in url:
                    continue
                    
                # Assess credibility based on domain
                domain = url.split('/')[2] if '/' in url else url
                credibility = self._assess_credibility(domain)
                
                evidence = Evidence(
                    title=result.get('title', 'Unknown'),
                    url=url,
                    snippet=result.get('body', '')[:200],
                    credibility=credibility
                )
                all_evidence.append(evidence)
                seen_urls.add(url)
        
        # Sort by credibility (high first)
        credibility_order = {"high": 0, "medium": 1, "low": 2}
        all_evidence.sort(key=lambda e: credibility_order.get(e.credibility or "medium", 1))
        
        logger.info(f"✅ Gathered {len(all_evidence)} evidence sources")
        return all_evidence[:10]  # Top 10 sources
    
    def _assess_credibility(self, domain: str) -> str:
        """Assess source credibility based on domain"""
        domain_lower = domain.lower()
        
        # High credibility sources - CRISIS MODE
        
        # 1. Official Government & Safety (India Focused)
        official_gov = ['gov.in', 'nic.in', 'police.gov.in', 'mha.gov.in', 'ndma.gov.in', 'who.int', 'pib.gov.in']
        
        # 2. Major Verified News & Wire Services
        major_news = ['reuters.com', 'ani', 'pti', 'thehindu.com', 'indianexpress.com', 'ndtv.com', 'ddnews.gov.in']
        
        # 3. Established Fact-Checkers
        fact_checkers = ['factcheck.org', 'snopes.com', 'politifact.com', 'altnews.in', 'boomlive.in', 'vishvasnews.com']
        
        # Combine high credibility lists
        high_cred = official_gov + major_news + fact_checkers
        
        if any(trusted in domain_lower for trusted in high_cred):
            return "high"
        
        # Low credibility sources
        low_cred = ['blog', 'wordpress', 'medium', 'facebook', 'twitter', 'reddit', 'tiktok', 'instagram', 'whatsapp']
        
        if any(untrusted in domain_lower for untrusted in low_cred):
            return "low"
        
        return "medium"

class MultiAIFactChecker(BaseAgent):
    """Fact checker using multiple AI models for consensus"""
    
    def __init__(self):
        super().__init__("MultiAIFactChecker")
        
        # Initialize Gemini
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Initialize Groq (free API)
        groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_client = Groq(api_key=groq_api_key) if groq_api_key else None
    
    @trace_operation("multi_ai_fact_checking")
    async def verify(self, claim: str, evidence: List[Evidence]) -> Dict:
        """Verify claim using multiple AI models"""
        logger.info(f"🔍 Multi-AI verification for: {claim}")
        
        evidence_summary = self._format_evidence(evidence)
        
        # Run both AI models in parallel
        tasks = [
            self._verify_with_gemini(claim, evidence_summary),
        ]
        
        if self.groq_client:
            tasks.append(self._verify_with_groq(claim, evidence_summary))
        
        verdicts = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out errors
        valid_verdicts = [v for v in verdicts if not isinstance(v, Exception)]
        
        if not valid_verdicts:
            logger.error("❌ All AI models failed")
            return {
                "final_verdict": "UNVERIFIED",
                "confidence": 0.0,
                "reasoning": "Unable to verify claim - all AI models failed",
                "ai_verdicts": []
            }
        
        # Calculate consensus
        consensus = self._calculate_consensus(valid_verdicts)
        
        logger.info(f"✅ Consensus: {consensus['final_verdict']} ({consensus['confidence']:.2f})")
        return consensus
    
    def _format_evidence(self, evidence: List[Evidence]) -> str:
        """Format evidence for AI prompt"""
        if not evidence:
            return "No evidence found."
        
        formatted = []
        for i, e in enumerate(evidence[:5], 1):
            formatted.append(f"{i}. [{e.credibility.upper()}] {e.title}\n   {e.snippet}\n   Source: {e.url}")
        
        return "\n\n".join(formatted)
    
    async def _verify_with_gemini(self, claim: str, evidence: str) -> AIVerdict:
        """Verify using Google Gemini"""
        prompt = f"""You are a Crisis Verification Expert. verify this incoming report during a potential emergency situation.

CLAIM: "{claim}"

EVIDENCE FROM SOURCES:
{evidence}

Determine the status of this claim based STRICTLY on the evidence provided:
- TRUE: Confirmed by official government sources or multiple reliable news outlets.
- FALSE: Debunked by official sources or police clarifications.
- MISLEADING: Contains grains of truth but is exaggerated or out of context.
- UNVERIFIED: No credible evidence found yet.

Return ONLY valid JSON:
{{
  "verdict": "FALSE",
  "confidence": 0.95,
  "reasoning": "Brief, urgent explanation focusing on public safety."
}}"""

        try:
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                prompt
            )
            
            result_text = response.text.strip()
            result_text = result_text.replace("```json", "").replace("```", "").strip()
            
            result = json.loads(result_text)
            
            return AIVerdict(
                model_name="Gemini 2.0 Flash",
                verdict=result['verdict'],
                confidence=float(result['confidence']),
                reasoning=result['reasoning']
            )
        except Exception as e:
            logger.error(f"❌ Gemini error: {e}")
            raise
    
    async def _verify_with_groq(self, claim: str, evidence: str) -> AIVerdict:
        """Verify using Groq (Llama)"""
        prompt = f"""You are a Crisis Verification Expert. verify this incoming report during a potential emergency situation.

CLAIM: "{claim}"

EVIDENCE FROM SOURCES:
{evidence}

Determine the status of this claim based STRICTLY on the evidence provided:
- TRUE: Confirmed by official government sources or multiple reliable news outlets.
- FALSE: Debunked by official sources or police clarifications.
- MISLEADING: Contains grains of truth but is exaggerated or out of context.
- UNVERIFIED: No credible evidence found yet.

Return ONLY valid JSON:
{{
  "verdict": "FALSE",
  "confidence": 0.95,
  "reasoning": "Brief, urgent explanation focusing on public safety."
}}"""

        try:
            response = await asyncio.to_thread(
                self.groq_client.chat.completions.create,
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content.strip()
            result_text = result_text.replace("```json", "").replace("```", "").strip()
            
            result = json.loads(result_text)
            
            return AIVerdict(
                model_name="Llama 3.3 70B",
                verdict=result['verdict'],
                confidence=float(result['confidence']),
                reasoning=result['reasoning']
            )
        except Exception as e:
            logger.error(f"❌ Groq error: {e}")
            raise
    
    def _calculate_consensus(self, verdicts: List[AIVerdict]) -> Dict:
        """Calculate consensus from multiple AI verdicts"""
        if not verdicts:
            return {
                "final_verdict": "UNVERIFIED",
                "confidence": 0.0,
                "reasoning": "No verdicts available",
                "ai_verdicts": []
            }
        
        # Count verdicts
        verdict_counts = {}
        for v in verdicts:
            verdict_counts[v.verdict] = verdict_counts.get(v.verdict, 0) + 1
        
        # Get majority verdict
        final_verdict = max(verdict_counts, key=verdict_counts.get)
        
        # Calculate average confidence for the majority verdict
        matching_verdicts = [v for v in verdicts if v.verdict == final_verdict]
        avg_confidence = sum(v.confidence for v in matching_verdicts) / len(matching_verdicts)
        
        # Combine reasoning
        reasoning_parts = [f"**{v.model_name}**: {v.reasoning}" for v in verdicts]
        combined_reasoning = "\n\n".join(reasoning_parts)
        
        return {
            "final_verdict": final_verdict,
            "confidence": avg_confidence,
            "reasoning": combined_reasoning,
            "ai_verdicts": verdicts
        }

class ExplainerAgent(BaseAgent):
    """Generates user-friendly explanations"""
    
    def __init__(self):
        super().__init__("Explainer")
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    @trace_operation("explanation_generation")
    async def explain(self, claim: str, verdict: str, reasoning: str, sources: List[Evidence]) -> str:
        """Generate clear, Community Notes-style explanation"""
        logger.info(f"📝 Generating explanation")
        
        sources_text = "\n".join([
            f"- [{s.title}]({s.url})"
            for s in sources[:3]
        ])
        
        prompt = f"""Create a clear, urgent Crisis Notification (Community Notes style):

Claim: "{claim}"
Verdict: {verdict}
AI Analysis: {reasoning}

Top Sources:
{sources_text}

Instructions:
1. Start with a clear verdict in bold (e.g., **FALSE: Confirmed as drill**).
2. Explain specifically what is happening and cite the official authority (e.g., "Mumbai Police confirmed...").
3. Warn against panic if necessary.
4. Keep it under 3 paragraphs.
5. Use Markdown."""

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"❌ Explanation error: {e}")
            return reasoning

class CoordinatorAgent(BaseAgent):
    """Main coordinator orchestrating all specialized agents"""
    
    def __init__(self):
        super().__init__("Coordinator")
        self.evidence_agent = EvidenceGathererAgent()
        self.fact_checker = MultiAIFactChecker()
        self.explainer_agent = ExplainerAgent()
        self.memory_bank = MemoryBank()
    
    @trace_operation("coordination")
    async def analyze(self, claim: str, url: Optional[str] = None) -> ClaimAnalysis:
        """
        Orchestrate multi-agent claim verification workflow
        
        1. Check memory for cached results
        2. Gather evidence from credible sources
        3. Multi-AI verification (Gemini + Groq)
        4. Generate explanation
        5. Store in memory
        """
        logger.info(f"🎯 Coordinating verification for: {claim}")
        
        # Step 1: Check memory
        cached_result = self.memory_bank.get(claim)
        if cached_result:
            logger.info(f"⚡ Retrieved from memory bank")
            return cached_result[0] if isinstance(cached_result, list) else cached_result
        
        # Step 2: Gather evidence
        logger.info(f"🚀 Gathering evidence")
        evidence = await self.evidence_agent.gather(claim)
        
        if not evidence:
            logger.warning(f"⚠️ No evidence found")
            return ClaimAnalysis(
                claim=claim,
                final_verdict="UNVERIFIED",
                confidence=0.0,
                explanation="Unable to find sufficient evidence to verify this claim.",
                ai_verdicts=[],
                sources=[],
                analyzed_at=datetime.now(),
                cached=False
            )
        
        # Step 3: Multi-AI verification
        verification = await self.fact_checker.verify(claim, evidence)
        
        # Step 4: Generate explanation
        explanation = await self.explainer_agent.explain(
            claim,
            verification['final_verdict'],
            verification['reasoning'],
            evidence
        )
        
        # Create analysis
        analysis = ClaimAnalysis(
            claim=claim,
            final_verdict=verification['final_verdict'],
            confidence=verification['confidence'],
            explanation=explanation,
            ai_verdicts=verification['ai_verdicts'],
            sources=evidence[:5],  # Top 5 sources
            analyzed_at=datetime.now(),
            cached=False
        )
        
        # Step 5: Store in memory
        self.memory_bank.store(claim, [analysis])
        logger.info(f"💾 Stored in memory bank")
        
        logger.info(f"✅ Verification complete: {verification['final_verdict']}")
        return analysis
