import { useState, useEffect } from 'react';

interface HeroProps {
    onVerify: (claim: string) => void;
    isLoading: boolean;
}

const Hero: React.FC<HeroProps> = ({ onVerify, isLoading }) => {
    const [claim, setClaim] = useState('');
    const [placeholder, setPlaceholder] = useState('');
    const [typingIndex, setTypingIndex] = useState(0);
    const [isDeleting, setIsDeleting] = useState(false);
    const [textLoopIndex, setTextLoopIndex] = useState(0);

    const examples = [
        "Mumbai flood warning...",
        "Riot reported in Bandra...",
        "Covid-19 new variant deadly...",
        "Earthquake tremor in Delhi..."
    ];

    useEffect(() => {
        const currentText = examples[textLoopIndex % examples.length];
        const typeSpeed = isDeleting ? 50 : 100;

        const timer = setTimeout(() => {
            if (!isDeleting && typingIndex < currentText.length) {
                setPlaceholder(currentText.substring(0, typingIndex + 1));
                setTypingIndex(prev => prev + 1);
            } else if (isDeleting && typingIndex > 0) {
                setPlaceholder(currentText.substring(0, typingIndex - 1));
                setTypingIndex(prev => prev - 1);
            } else if (!isDeleting && typingIndex === currentText.length) {
                setTimeout(() => setIsDeleting(true), 1500);
            } else if (isDeleting && typingIndex === 0) {
                setIsDeleting(false);
                setTextLoopIndex(prev => prev + 1);
            }
        }, typeSpeed);

        return () => clearTimeout(timer);
    }, [typingIndex, isDeleting, textLoopIndex]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (claim.trim()) {
            onVerify(claim);
        }
    };

    return (
        <div className="relative py-20 lg:py-32 overflow-hidden">
            {/* Background Gradients */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-blue-600/10 dark:bg-blue-600/20 rounded-full blur-[100px] -z-10" />

            <div className="max-w-4xl mx-auto px-4 text-center">
                <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
                    <span className="text-slate-900 dark:text-white">Verify Crisis Info with </span>
                    <span className="bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent">
                        Official Sources
                    </span>
                </h1>

                <p className="text-lg md:text-xl text-slate-600 dark:text-slate-400 mb-12 max-w-2xl mx-auto">
                    Stop the panic. Instant verification for floods, riots, and emergency situations using official government data.
                </p>

                <form onSubmit={handleSubmit} className="relative max-w-2xl mx-auto group">
                    <div className="absolute inset-0 bg-gradient-to-r from-red-500 to-orange-500 rounded-xl blur opacity-25 group-hover:opacity-40 transition duration-1000"></div>
                    <div className="relative bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-700 shadow-xl dark:shadow-2xl flex items-center p-2 transition-colors">
                        <input
                            type="text"
                            value={claim}
                            onChange={(e) => setClaim(e.target.value)}
                            placeholder={placeholder}
                            className="flex-1 bg-transparent border-none text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:ring-0 text-lg px-4 py-2"
                            disabled={isLoading}
                        />
                        <button
                            type="submit"
                            disabled={isLoading || !claim.trim()}
                            className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-lg font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shadow-lg shadow-blue-500/20"
                        >
                            {isLoading ? (
                                <>
                                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Verifying...
                                </>
                            ) : (
                                'Verify'
                            )}
                        </button>
                    </div>
                </form>

                <div className="mt-8 flex justify-center gap-4 text-sm text-slate-500 dark:text-slate-500">
                    <span className="flex items-center gap-1">
                        <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                        Live Web Search
                    </span>
                    <span className="flex items-center gap-1">
                        <svg className="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                        Multi-Agent Analysis
                    </span>
                </div>
            </div>
        </div>
    );
};

export default Hero;
