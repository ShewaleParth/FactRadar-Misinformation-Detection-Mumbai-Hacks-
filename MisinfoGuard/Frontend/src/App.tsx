import { useState } from 'react';
import Layout from './components/Layout';
import Hero from './components/Hero';
import AnalysisResult from './components/AnalysisResult';
import HowItWorks from './components/HowItWorks';
import About from './components/About';
import type { ClaimAnalysis } from './types';

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ClaimAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleVerify = async (claim: string) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // In a real staging environment we would use an environment variable
      // For localhost development, this is fine
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ claim, url: null }),
      });

      if (!response.ok) {
        throw new Error('Analysis failed. Please try again.');
      }

      const data = await response.json();
      setResult(data.analysis);

      // Smooth scroll to result
      setTimeout(() => {
        document.getElementById('result-section')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <Hero onVerify={handleVerify} isLoading={loading} />

      {error && (
        <div className="max-w-xl mx-auto mb-12 px-4 fade-in">
          <div className="bg-red-500/10 border border-red-500/20 text-red-200 px-6 py-4 rounded-xl flex items-center gap-3">
            <svg className="w-6 h-6 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            {error}
          </div>
        </div>
      )}

      {result && (
        <div id="result-section" className="min-h-[600px] bg-slate-950/30 border-t border-slate-900 py-20 relative">
          <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-blue-500/20 to-transparent"></div>
          <AnalysisResult result={result} />
        </div>
      )}

      <HowItWorks />
      <About />
    </Layout>
  );
}

export default App;
