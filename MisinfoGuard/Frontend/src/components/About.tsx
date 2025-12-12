import React from 'react';

const About: React.FC = () => {
    return (
        <section id="about" className="py-20 bg-slate-50 dark:bg-slate-900/30 transition-colors">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="grid md:grid-cols-2 gap-16 items-center">
                    <div>
                        <h2 className="text-3xl md:text-5xl font-bold mb-6">
                            <span className="text-slate-900 dark:text-white">Why We Built </span>
                            <span className="bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent">
                                MisinfoGuard
                            </span>
                        </h2>
                        <div className="space-y-6 text-slate-600 dark:text-slate-400 text-lg leading-relaxed">
                            <p>
                                In times of crisis-floods, riots, or pandemics-misinformation spreads faster than the truth. False rumors can cause panic, confusion, and even loss of life.
                            </p>
                            <p>
                                <strong className="text-slate-900 dark:text-slate-200">Our Mission:</strong> To provide a centralized, instant verification shield that prioritizes official government channels and vetted sources over viral social media noise.
                            </p>
                            <p>
                                Built for the <strong className="text-slate-900 dark:text-white">Mumbai Hacks</strong> initiative, we are leveraging cutting-edge Agentic AI to serve the public interest.
                            </p>
                        </div>
                    </div>

                    <div className="relative">
                        <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 rounded-2xl blur-3xl opacity-20"></div>
                        <div className="relative bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 shadow-2xl transition-colors">
                            <div className="space-y-6">
                                <div className="flex items-start gap-4">
                                    <div className="w-12 h-12 rounded-full bg-red-500/10 flex items-center justify-center border border-red-500/20 shrink-0">
                                        🛡️
                                    </div>
                                    <div>
                                        <h3 className="text-slate-900 dark:text-white font-bold text-lg">Crisis-First Approach</h3>
                                        <p className="text-slate-600 dark:text-slate-400 mt-1">Focus on safety-critical information during emergencies.</p>
                                    </div>
                                </div>

                                <div className="flex items-start gap-4">
                                    <div className="w-12 h-12 rounded-full bg-blue-500/10 flex items-center justify-center border border-blue-500/20 shrink-0">
                                        👮
                                    </div>
                                    <div>
                                        <h3 className="text-slate-900 dark:text-white font-bold text-lg">Official Data Verification</h3>
                                        <p className="text-slate-600 dark:text-slate-400 mt-1">Direct integration with Police & Government notification patterns.</p>
                                    </div>
                                </div>

                                <div className="flex items-start gap-4">
                                    <div className="w-12 h-12 rounded-full bg-green-500/10 flex items-center justify-center border border-green-500/20 shrink-0">
                                        ⚡
                                    </div>
                                    <div>
                                        <h3 className="text-slate-900 dark:text-white font-bold text-lg">Real-Time Response</h3>
                                        <p className="text-slate-600 dark:text-slate-400 mt-1">Instant analysis when milliseconds matter.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default About;
