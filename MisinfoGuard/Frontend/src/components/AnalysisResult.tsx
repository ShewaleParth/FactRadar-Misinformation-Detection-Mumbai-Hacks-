import type { ClaimAnalysis } from '../types';
import ReactMarkdown from 'react-markdown';

interface AnalysisResultProps {
    result: ClaimAnalysis;
}

const AnalysisResult: React.FC<AnalysisResultProps> = ({ result }) => {
    // Map API verdicts to User-Friendly Terms and Colors
    const verdictConfig = {
        'TRUE': {
            label: 'REAL',
            color: 'text-green-600 dark:text-green-400',
            bg: 'bg-green-50 dark:bg-green-500/10',
            border: 'border-green-200 dark:border-green-500/20',
            icon: '✅'
        },
        'FALSE': {
            label: 'MISINFORMATION',
            color: 'text-red-600 dark:text-red-400',
            bg: 'bg-red-50 dark:bg-red-500/10',
            border: 'border-red-200 dark:border-red-500/20',
            icon: '❌'
        },
        'MISLEADING': {
            label: 'MISLEADING',
            color: 'text-yellow-600 dark:text-yellow-400',
            bg: 'bg-yellow-50 dark:bg-yellow-500/10',
            border: 'border-yellow-200 dark:border-yellow-500/20',
            icon: '⚠️'
        },
        'UNVERIFIED': {
            label: 'UNCERTAIN',
            color: 'text-slate-600 dark:text-slate-400',
            bg: 'bg-slate-50 dark:bg-slate-500/10',
            border: 'border-slate-200 dark:border-slate-500/20',
            icon: '❓'
        }
    };

    const config = verdictConfig[result.final_verdict] || verdictConfig['UNVERIFIED'];

    return (
        <div className="max-w-3xl mx-auto px-4 pb-20 fade-in">
            {/* Verdict Card */}
            <div className={`rounded-2xl border ${config.border} ${config.bg} p-8 mb-8 text-center transition-colors shadow-sm`}>
                <div className="text-6xl mb-4">{config.icon}</div>
                <h2 className={`text-4xl font-extrabold tracking-wide ${config.color} mb-2`}>
                    {config.label}
                </h2>
                <p className="text-slate-600 dark:text-slate-400 flex items-center justify-center gap-2">
                    <span>Confidence Score:</span>
                    <span className="font-mono text-slate-900 dark:text-white">{(result.confidence * 100).toFixed(0)}%</span>
                </p>
            </div>

            {/* AI Summary - "Community Notes" Style */}
            <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-700 overflow-hidden mb-8 shadow-lg dark:shadow-none transition-colors">
                <div className="bg-slate-50 dark:bg-slate-800/50 px-6 py-4 border-b border-slate-200 dark:border-slate-700 flex items-center justify-between">
                    <h3 className="font-semibold text-lg flex items-center gap-2 text-slate-800 dark:text-slate-200">
                        <span className="text-blue-500 dark:text-blue-400">✨</span> AI Analysis Summary
                    </h3>
                    <span className="text-xs text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded border border-slate-200 dark:border-slate-700">Community Note Style</span>
                </div>
                <div className="p-6 text-slate-700 dark:text-slate-300 prose prose-slate dark:prose-invert max-w-none">
                    <ReactMarkdown>{result.explanation}</ReactMarkdown>
                </div>
            </div>

            {/* Sources */}
            <div className="space-y-4">
                <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-4">Credible Sources</h3>
                {result.sources.length === 0 ? (
                    <p className="text-slate-500 italic">No specific sources cited.</p>
                ) : (
                    result.sources.map((source, idx) => (
                        <a
                            key={idx}
                            href={source.url}
                            target="_blank"
                            rel="noreferrer"
                            className="block bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600 rounded-xl p-4 transition-all group shadow-sm hover:shadow-md dark:shadow-none"
                        >
                            <div className="flex items-start justify-between gap-4">
                                <div>
                                    <h4 className="font-medium text-blue-400 group-hover:text-blue-300 mb-1">
                                        {source.title || 'Untitled Source'}
                                    </h4>
                                    <p className="text-sm text-slate-400 line-clamp-2 mb-2">
                                        {source.snippet}
                                    </p>
                                    <div className="flex items-center gap-2">
                                        {source.credibility === 'high' && (
                                            <span className="text-xs bg-green-900/40 text-green-400 px-2 py-0.5 rounded border border-green-900/50">
                                                High Credibility
                                            </span>
                                        )}
                                        <span className="text-xs text-slate-600 truncate max-w-[200px]">
                                            {source.url}
                                        </span>
                                    </div>
                                </div>
                                <svg className="w-5 h-5 text-slate-600 group-hover:text-slate-400 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                </svg>
                            </div>
                        </a>
                    ))
                )}
            </div>
        </div>
    );
};

export default AnalysisResult;
