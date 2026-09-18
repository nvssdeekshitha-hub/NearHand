import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
    HeartPulse, 
    Shield, 
    Sparkles, 
    Users, 
    Mic, 
    Activity, 
    Clock, 
    CheckCircle2, 
    UserCheck, 
    AlertTriangle, 
    ChevronRight, 
    Heart,
    Zap
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

function Navbar() {
    const navigate = useNavigate();
    return (
        <nav className="fixed w-full bg-white/90 backdrop-blur-md border-b border-slate-200 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-20">
                    <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate('/')}>
                        <div className="w-10 h-10 rounded-xl bg-sky-50 border border-sky-200 flex items-center justify-center">
                            <HeartPulse className="w-6 h-6 text-sky-600" />
                        </div>
                        <span className="font-black text-2xl tracking-tight text-slate-900">NEARHAND</span>
                    </div>

                    <div className="hidden md:flex space-x-8 text-sm font-semibold text-slate-600">
                        <a href="#features" className="hover:text-sky-600 transition-colors">Features</a>
                        <a href="#how-it-works" className="hover:text-sky-600 transition-colors">How It Works</a>
                        <a href="#innovation" className="hover:text-sky-600 transition-colors">Fail-Safe Escalation</a>
                        <a href="#multilingual" className="hover:text-sky-600 transition-colors">Voice AI</a>
                    </div>

                    <div className="flex items-center space-x-3">
                        <Button variant="ghost" onClick={() => navigate('/login')} className="hidden sm:inline-flex text-xs font-bold">
                            Sign In
                        </Button>
                        <Button onClick={() => navigate('/login')} className="text-xs font-bold px-5 bg-sky-600 hover:bg-sky-700 text-white rounded-xl shadow-sm">
                            Get Started →
                        </Button>
                    </div>
                </div>
            </div>
        </nav>
    );
}

// Interactive Network Visualization
function NetworkVisualization() {
    return (
        <div className="relative w-full aspect-square md:aspect-[4/3] flex items-center justify-center">
            {/* Pulsing Backglow */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-72 h-72 bg-sky-400/10 rounded-full blur-3xl -z-10 animate-pulse"></div>

            {/* Network Nodes */}
            <div className="absolute top-4 right-6 bg-white shadow-lg p-3 px-4 rounded-2xl flex items-center space-x-3 border border-slate-100 animate-fade-in">
                <div className="w-9 h-9 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center font-bold">
                    <Activity className="w-5 h-5" />
                </div>
                <div>
                    <p className="text-xs font-bold text-slate-900">Caretaker Ravi</p>
                    <p className="text-[10px] text-emerald-600 font-semibold">🟢 Connected</p>
                </div>
            </div>

            <div className="absolute bottom-6 left-4 bg-white shadow-lg p-3 px-4 rounded-2xl flex items-center space-x-3 border border-slate-100 animate-fade-in">
                <div className="w-9 h-9 bg-amber-50 text-amber-600 rounded-xl flex items-center justify-center font-bold">
                    <Users className="w-5 h-5" />
                </div>
                <div>
                    <p className="text-xs font-bold text-slate-900">Volunteer Priya</p>
                    <p className="text-[10px] text-amber-600 font-semibold">2.4 km • Standby</p>
                </div>
            </div>

            <div className="absolute top-6 left-6 bg-white shadow-lg p-3 px-4 rounded-2xl flex items-center space-x-3 border border-slate-100 animate-fade-in">
                <div className="w-9 h-9 bg-rose-50 text-rose-600 rounded-xl flex items-center justify-center font-bold">
                    <Heart className="w-5 h-5" />
                </div>
                <div>
                    <p className="text-xs font-bold text-slate-900">Family Anjali</p>
                    <p className="text-[10px] text-slate-400 font-semibold">Notified</p>
                </div>
            </div>

            {/* Main Floating Request Card */}
            <Card className="relative z-10 w-80 shadow-2xl border-2 border-sky-100 bg-white/95 backdrop-blur p-6 rounded-3xl">
                <div className="flex justify-between items-center mb-4 border-b border-slate-100 pb-3">
                    <span className="text-[10px] font-bold text-slate-400 tracking-wider uppercase">Active Request</span>
                    <Badge variant="critical">CRITICAL</Badge>
                </div>

                <div className="space-y-3.5">
                    <div>
                        <h3 className="font-extrabold text-slate-900 text-lg">Lakshmi, 72</h3>
                        <p className="text-xs text-slate-600 font-medium">Fall / Unable to stand</p>
                    </div>

                    <div className="flex justify-between items-center bg-slate-50 p-2.5 rounded-xl border border-slate-100 text-xs">
                        <span className="text-slate-500 font-medium">Risk Score</span>
                        <span className="font-bold text-rose-600">94 / 100</span>
                    </div>

                    <div className="space-y-1.5 text-xs font-semibold">
                        <div className="flex items-center text-emerald-600">
                            <CheckCircle2 className="w-4 h-4 mr-2" /> 
                            <span className="text-slate-700">AI Urgency Analyzed</span>
                        </div>
                        <div className="flex items-center text-emerald-600">
                            <CheckCircle2 className="w-4 h-4 mr-2" /> 
                            <span className="text-slate-700">Caretaker Ravi Notified</span>
                        </div>
                    </div>

                    <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                        <span className="text-xs text-slate-400 font-medium">Response Target:</span>
                        <span className="text-xl font-mono font-black text-sky-600">01:24</span>
                    </div>
                </div>
            </Card>
        </div>
    );
}

// Innovation Section Tracker (Part 30)
function InnovationShowcase() {
    const [step, setStep] = useState(0);

    const handleNext = () => {
        if (step < 5) setStep(step + 1);
        else setStep(0);
    };

    return (
        <div className="bg-slate-900 text-white rounded-3xl p-8 md:p-12 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-sky-500 rounded-full mix-blend-screen filter blur-[120px] opacity-20"></div>

            <div className="relative z-10 grid md:grid-cols-2 gap-10 items-center">
                <div>
                    <span className="text-xs font-black text-sky-400 uppercase tracking-widest block mb-2">
                        Dynamic Care Fallback
                    </span>
                    <h2 className="text-3xl sm:text-4xl font-extrabold mb-4 tracking-tight leading-tight">
                        When the first plan fails,<br />
                        <span className="text-sky-400">NEARHAND adapts.</span>
                    </h2>
                    <p className="text-sm sm:text-base text-slate-400 mb-8 leading-relaxed max-w-lg">
                        Seniors shouldn't have to wait when help is delayed. When a primary caretaker does not acknowledge within the target response window, our AI dynamically activates verified nearby community volunteers without missing a beat.
                    </p>

                    <Button 
                        onClick={handleNext}
                        className="bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm px-6 py-3.5 rounded-2xl shadow-lg border-0"
                    >
                        {step === 0 ? 'SIMULATE CARETAKER TIMEOUT' : step === 5 ? 'RESET WORKFLOW' : 'CONTINUE STEP'}
                        <ChevronRight className="w-4 h-4 ml-2" />
                    </Button>
                </div>

                {/* Interactive Workflow Diagram */}
                <div className="bg-slate-800/90 border border-slate-700 rounded-3xl p-6 space-y-4">
                    <div className="flex items-center space-x-3 text-xs font-semibold text-slate-300">
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                        <span>1. Senior Request Captured (Telugu Voice Input)</span>
                    </div>

                    <div className="flex items-center space-x-3 text-xs font-semibold text-slate-300">
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                        <span>2. AI Priority Assessed (CRITICAL 94/100)</span>
                    </div>

                    <div className="flex items-center space-x-3 text-xs font-semibold text-slate-300">
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                        <span>3. Caretaker Ravi Notified</span>
                    </div>

                    {step === 0 && (
                        <div className="p-3.5 bg-slate-700/60 rounded-2xl border border-slate-600 flex items-center space-x-3 text-xs">
                            <Clock className="w-4 h-4 text-sky-400 animate-spin-slow" />
                            <span className="font-bold text-sky-300">Waiting for response (02:00 window active)</span>
                        </div>
                    )}

                    {step >= 1 && (
                        <div className="p-3.5 bg-rose-950/40 rounded-2xl border border-rose-800 text-rose-300 flex items-center space-x-3 text-xs animate-fade-in font-bold">
                            <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0" />
                            <span>4. Caretaker timeout expired. Escalating...</span>
                        </div>
                    )}

                    {step >= 2 && (
                        <div className="p-3.5 bg-sky-950/40 rounded-2xl border border-sky-800 text-sky-300 flex items-center space-x-3 text-xs animate-fade-in font-bold">
                            <Zap className="w-4 h-4 text-sky-400 shrink-0" />
                            <span>5. Nearby Volunteer Priya Sharma matched (2.4 km, ETA 7 min)</span>
                        </div>
                    )}

                    {step >= 3 && (
                        <div className="p-3.5 bg-emerald-950/40 rounded-2xl border border-emerald-800 text-emerald-300 flex items-center space-x-3 text-xs animate-fade-in font-bold">
                            <UserCheck className="w-4 h-4 text-emerald-400 shrink-0" />
                            <span>6. Volunteer Priya accepted • Family Anjali alerted</span>
                        </div>
                    )}

                    {step >= 4 && (
                        <div className="p-3.5 bg-emerald-900/60 rounded-2xl border border-emerald-600 text-white flex items-center space-x-3 text-xs animate-fade-in font-bold">
                            <CheckCircle2 className="w-4 h-4 text-emerald-300 shrink-0" />
                            <span>7. Request resolved • Archived to History</span>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export function LandingPage() {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-slate-50 font-sans selection:bg-sky-500 selection:text-white">
            <Navbar />

            {/* Hero Section (Part 28) */}
            <section className="pt-32 pb-20 md:pt-40 md:pb-28 overflow-hidden relative">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid lg:grid-cols-2 gap-12 lg:gap-8 items-center">
                        
                        {/* Text Col */}
                        <div className="text-center lg:text-left z-10 relative">
                            <div className="inline-flex items-center px-3.5 py-1.5 rounded-full bg-sky-50 border border-sky-200 text-sky-700 font-bold text-xs mb-6 uppercase tracking-wider">
                                <Sparkles className="w-3.5 h-3.5 mr-1.5 text-sky-600" /> AI-Powered Senior Care
                            </div>

                            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-slate-900 tracking-tight leading-[1.15] mb-6">
                                The right help.<br />
                                At the right time.<br />
                                <span className="text-sky-600 inline-block mt-1">
                                    For every senior.
                                </span>
                            </h1>

                            <p className="text-base sm:text-lg text-slate-600 mb-8 leading-relaxed max-w-xl mx-auto lg:mx-0 font-medium">
                                NEARHAND understands what seniors need through natural voice, connects them with their dedicated caretaker, and activates verified nearby community volunteers when urgent help doesn't arrive.
                            </p>

                            <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-3.5 mb-10">
                                <Button 
                                    size="lg" 
                                    className="w-full sm:w-auto px-8 py-4 text-base font-bold bg-sky-600 hover:bg-sky-700 text-white rounded-2xl shadow-lg shadow-sky-600/20"
                                    onClick={() => navigate('/login')}
                                >
                                    Get Started →
                                </Button>
                                <a 
                                    href="#innovation"
                                    className="w-full sm:w-auto px-6 py-3.5 text-center font-bold text-slate-700 bg-white border border-slate-200 rounded-2xl hover:bg-slate-50 transition-colors text-base shadow-xs"
                                >
                                    See How It Works
                                </a>
                            </div>

                            <div className="flex flex-wrap items-center justify-center lg:justify-start gap-6 text-xs font-bold text-slate-500">
                                <span className="flex items-center"><Shield className="w-4 h-4 mr-1.5 text-emerald-600" /> Trusted Caregivers</span>
                                <span className="flex items-center"><Users className="w-4 h-4 mr-1.5 text-sky-600" /> Community Fallback</span>
                                <span className="flex items-center"><Clock className="w-4 h-4 mr-1.5 text-amber-500" /> Rapid Dispatch</span>
                            </div>
                        </div>

                        {/* Visual Col */}
                        <div>
                            <NetworkVisualization />
                        </div>

                    </div>
                </div>
            </section>

            {/* Feature Section: 3 Major Cards (Part 29) */}
            <section id="features" className="py-20 bg-white border-y border-slate-100">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center max-w-2xl mx-auto mb-14">
                        <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight mb-3">
                            Care that thinks ahead.
                        </h2>
                        <p className="text-base text-slate-600 font-medium">
                            From instant voice capture to fail-safe volunteer escalation.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-6">
                        <Card className="p-8 border-slate-200 hover:border-sky-300 transition-all shadow-xs hover:shadow-md">
                            <div className="w-14 h-14 rounded-2xl bg-sky-50 text-sky-600 flex items-center justify-center mb-6">
                                <Mic className="w-7 h-7" />
                            </div>
                            <h3 className="text-xl font-bold text-slate-900 mb-2">01 — UNDERSTAND</h3>
                            <p className="text-sm text-slate-600 leading-relaxed font-medium">
                                Multilingual text and native browser voice requests let seniors ask for help naturally in Telugu, Hindi, English, Tamil, Kannada, or Malayalam.
                            </p>
                        </Card>

                        <Card className="p-8 border-slate-200 hover:border-sky-300 transition-all shadow-xs hover:shadow-md">
                            <div className="w-14 h-14 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-6">
                                <Sparkles className="w-7 h-7" />
                            </div>
                            <h3 className="text-xl font-bold text-slate-900 mb-2">02 — COORDINATE</h3>
                            <p className="text-sm text-slate-600 leading-relaxed font-medium">
                                AI-assisted urgency analysis evaluates risk signals (e.g. falls, medication omissions) and matches the request with primary caretakers immediately.
                            </p>
                        </Card>

                        <Card className="p-8 border-slate-200 hover:border-sky-300 transition-all shadow-xs hover:shadow-md">
                            <div className="w-14 h-14 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center mb-6">
                                <Users className="w-7 h-7" />
                            </div>
                            <h3 className="text-xl font-bold text-slate-900 mb-2">03 — ESCALATE</h3>
                            <p className="text-sm text-slate-600 leading-relaxed font-medium">
                                Automatic fallback when the caretaker doesn't respond. Certified nearby community volunteers are notified with privacy safeguards.
                            </p>
                        </Card>
                    </div>
                </div>
            </section>

            {/* Innovation Section (Part 30) */}
            <section id="innovation" className="py-20 bg-slate-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <InnovationShowcase />
                </div>
            </section>

            {/* Multilingual Voice AI Showcase (Part 31) */}
            <section id="multilingual" className="py-20 bg-white border-b border-slate-100">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid lg:grid-cols-2 gap-12 items-center">
                        
                        {/* Sample Card */}
                        <div>
                            <Card className="p-6 md:p-8 border-2 border-sky-200 shadow-xl bg-white rounded-3xl">
                                <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100 mb-4">
                                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Senior Voice Sample</span>
                                    <p className="text-xl font-bold text-slate-900 italic font-serif">
                                        "Nenu bathroom lo padipoyanu, levalekapothunnanu."
                                    </p>
                                </div>

                                <div className="space-y-2.5 text-xs">
                                    <div className="flex justify-between py-2 border-b border-slate-100">
                                        <span className="text-slate-500 font-semibold">Language</span>
                                        <span className="font-bold text-slate-900">Telugu (te-IN)</span>
                                    </div>
                                    <div className="flex justify-between py-2 border-b border-slate-100">
                                        <span className="text-slate-500 font-semibold">AI Urgency</span>
                                        <span className="font-bold text-rose-600">CRITICAL</span>
                                    </div>
                                    <div className="flex justify-between py-2 border-b border-slate-100">
                                        <span className="text-slate-500 font-semibold">AI Priority Score</span>
                                        <span className="font-bold text-rose-600">94 / 100</span>
                                    </div>
                                    <div className="flex justify-between py-2">
                                        <span className="text-slate-500 font-semibold">Target Response Window</span>
                                        <span className="font-mono font-bold text-sky-600">02:00</span>
                                    </div>
                                </div>
                            </Card>
                        </div>

                        {/* Description */}
                        <div>
                            <span className="text-xs font-black text-sky-600 uppercase tracking-widest block mb-2">
                                Multilingual Natural Voice Input
                            </span>
                            <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight mb-4">
                                Speak naturally. NEARHAND understands.
                            </h2>
                            <p className="text-sm sm:text-base text-slate-600 leading-relaxed mb-6 font-medium">
                                Seniors shouldn't need to struggle with complex navigation during distress. They can speak naturally in Telugu, Hindi, Tamil, Kannada, Malayalam, or English.
                            </p>

                            <div className="flex flex-wrap gap-2">
                                {['English', 'తెలుగు (Telugu)', 'हिन्दी (Hindi)', 'தமிழ் (Tamil)', 'ಕನ್ನಡ (Kannada)', 'മലയാളം (Malayalam)'].map(l => (
                                    <span key={l} className="px-3.5 py-1.5 bg-slate-100 text-slate-700 rounded-xl text-xs font-bold border border-slate-200">
                                        {l}
                                    </span>
                                ))}
                            </div>
                        </div>

                    </div>
                </div>
            </section>

            {/* How It Works (Part 28) */}
            <section id="how-it-works" className="py-20 bg-slate-50">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 className="text-3xl font-extrabold text-slate-900 mb-10">
                        Seamless Coordination Flow
                    </h2>

                    <div className="space-y-3">
                        {[
                            { num: '01', title: 'Senior speaks or types assistance request' },
                            { num: '02', title: 'AI analyzes urgency & assigns priority score' },
                            { num: '03', title: 'Primary Caretaker receives instant notification & response timer' },
                            { num: '04', title: 'If caretaker does not respond, automatic volunteer escalation triggers' },
                            { num: '05', title: 'Nearby verified volunteer accepts & family is notified' },
                            { num: '06', title: 'Request is resolved and archived in Request History' },
                        ].map((item) => (
                            <div key={item.num} className="p-4 bg-white rounded-2xl border border-slate-200 flex items-center space-x-4 shadow-xs text-left">
                                <div className="w-10 h-10 rounded-xl bg-sky-50 text-sky-700 font-black flex items-center justify-center shrink-0 text-sm">
                                    {item.num}
                                </div>
                                <p className="font-bold text-slate-900 text-sm sm:text-base">{item.title}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-slate-900 text-white py-16 text-center">
                <div className="max-w-3xl mx-auto px-4">
                    <HeartPulse className="w-10 h-10 text-sky-400 mx-auto mb-4" />
                    <h2 className="text-2xl sm:text-3xl font-bold mb-4">
                        Experience NEARHAND in Action
                    </h2>
                    <Button 
                        size="lg" 
                        onClick={() => navigate('/login')}
                        className="bg-sky-600 hover:bg-sky-500 font-bold px-8 py-3.5 rounded-2xl"
                    >
                        Launch Interactive Demo
                    </Button>
                    <p className="text-xs text-slate-500 mt-10">
                        &copy; 2026 NEARHAND. AI Senior Care Coordination Platform. Built for HealthTech Hackathon.
                    </p>
                </div>
            </footer>
        </div>
    );
}
