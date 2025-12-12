export interface Evidence {
    title: string;
    url: string;
    snippet: string;
    credibility: 'high' | 'medium' | 'low' | null;
}

export interface ClaimAnalysis {
    claim: string;
    final_verdict: 'TRUE' | 'FALSE' | 'MISLEADING' | 'UNVERIFIED';
    confidence: number;
    explanation: string;
    sources: Evidence[];
    analyzed_at: string;
    cached: boolean;
}

export interface AnalysisResponse {
    analysis: ClaimAnalysis;
    processing_time: number;
    cached: boolean;
}
