import React from 'react';

const HowItWorks: React.FC = () => {
    const steps = [
        {
            title: "1. Scan & Detect",
            description: "We instantly scan your claim against official government sources (NDMA, Police, Ministry of Health) and vetted news outlets.",
            icon: "🔍"
        },
        {
            title: "2. Multi-Agent Verification",
            description: "Our AI agents analyze the credibility of sources, cross-referencing multiple reports to filter out fake news and rumors.",
            icon: "🤖"
        },
        {
            title: "3. Verified Verdict",
            description: "You get a clear 'REAL', 'MISINFORMATION', or 'UNCERTAIN' verdict with a summary explaining why, backed by direct links.",
            icon: "✅"
        }
    ];

    return (
        <section id="how-it-works" className="py-20 relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-blue-500/10 to-transparent"></div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
                <div className="text-center mb-16">
                    <h2 className="text-3xl md:text-5xl font-bold mb-4">
                        <span className="text-slate-900 dark:text-white">How </span>
                        <span className="bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400 bg-clip-text text-transparent">
                            MisinfoGuard Works
                        </span>
                    </h2>
                    <p className="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
                        Powered by a sophisticated Multi-Agent AI architecture ensuring you only get verified information during critical times.
                    </p>
                </div>

                <div className="grid md:grid-cols-3 gap-8">
                    {steps.map((step, idx) => (
                        <div key={idx} className="bg-white dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 p-8 rounded-2xl hover:border-slate-300 dark:hover:border-slate-700 transition-colors relative group shadow-lg dark:shadow-none">
                            <div className="absolute inset-0 bg-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl"></div>
                            <div className="text-4xl mb-6 bg-slate-100 dark:bg-slate-800 w-16 h-16 rounded-xl flex items-center justify-center border border-slate-200 dark:border-slate-700 shadow-md dark:shadow-lg">
                                {step.icon}
                            </div>
                            <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">{step.title}</h3>
                            <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                                {step.description}
                            </p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default HowItWorks;
