import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
    Mic, 
    Square, 
    Send, 
    Sparkles, 
    Globe2, 
    AlertCircle, 
    RotateCcw, 
    CheckCircle2, 
    ArrowLeft, 
    Keyboard
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Card } from '../../components/ui/Card';
import { useSpeechRecognition } from '../../hooks/useSpeechRecognition';
import { useCare } from '../../context/CareContext';
import { AIAnalysisCard } from '../../components/ai/AIAnalysisCard';

const LANGUAGES = [
    { code: 'te-IN', name: 'Telugu', nativeName: 'తెలుగు', sample: 'Nenu bathroom lo padipoyanu, levalekapothunnanu.' },
    { code: 'en-IN', name: 'English', nativeName: 'English', sample: 'I fell in the bathroom and I cannot stand up.' },
    { code: 'hi-IN', name: 'Hindi', nativeName: 'हिन्दी', sample: 'Main bathroom mein gir gayi hoon aur khadi nahi ho pa rahi.' },
    { code: 'ta-IN', name: 'Tamil', nativeName: 'தமிழ்', sample: 'Naan kuliyalaraiel vizhundhu vitten, ezhundhirukka mudiyavillai.' },
    { code: 'kn-IN', name: 'Kannada', nativeName: 'ಕನ್ನಡ', sample: 'Naanu bathroom nalli bididdene, eddelu sadhyavaguttilla.' },
    { code: 'ml-IN', name: 'Malayalam', nativeName: 'മലയാളം', sample: 'Njan bathroomil veenu, ezhunelkkan pattunnilla.' },
];

export function SeniorRequest() {
    const navigate = useNavigate();
    const { submitSeniorRequest } = useCare();

    const [selectedLanguage, setSelectedLanguage] = useState(LANGUAGES[0]); // Telugu by default
    const [textInput, setTextInput] = useState('');
    const [step, setStep] = useState('input'); // 'input' | 'analyzing' | 'complete'
    const [createdRequest, setCreatedRequest] = useState(null);

    const {
        isSupported,
        isListening,
        transcript,
        interimTranscript,
        error: speechError,
        formattedDuration,
        startListening,
        stopListening,
        resetTranscript,
        setTranscript
    } = useSpeechRecognition();

    // Sync speech transcript into textInput
    useEffect(() => {
        if (transcript) {
            setTextInput(transcript);
        }
    }, [transcript]);

    const handleStartRecording = () => {
        resetTranscript();
        startListening(selectedLanguage.code);
    };

    const handleStopRecording = () => {
        stopListening();
    };

    const handlePresetClick = (sampleText) => {
        stopListening();
        setTranscript(sampleText);
        setTextInput(sampleText);
    };

    const handleSubmit = async () => {
        const textToSubmit = textInput.trim() || transcript.trim() || selectedLanguage.sample;
        if (!textToSubmit) return;

        setStep('analyzing');

        // Assess urgency based on keywords
        const lower = textToSubmit.toLowerCase();
        const isFall = lower.includes('fall') || lower.includes('padipoyanu') || lower.includes('gir') || lower.includes('bathroom') || lower.includes('stand');
        const isMed = lower.includes('med') || lower.includes('pill') || lower.includes('insulin') || lower.includes('dose');

        const requestType = isFall ? 'Fall' : isMed ? 'Medication' : 'Assistance';
        const category = isFall ? 'Emergency' : isMed ? 'Medication' : 'Assistance';
        const urgency = isFall ? 'CRITICAL' : isMed ? 'WARNING' : 'MEDIUM';
        const riskScore = isFall ? 94 : isMed ? 65 : 45;
        const targetSeconds = isFall ? 120 : isMed ? 600 : 900;
        const explanation = isFall 
            ? 'The senior reports a fall and inability to stand. Immediate physical assessment required.'
            : 'Care coordination signals detected. Caretaker alerted within target response timeframe.';

        setTimeout(async () => {
            const req = await submitSeniorRequest({
                transcript: textToSubmit,
                language: selectedLanguage.name,
                request_type: requestType,
                category,
                urgency,
                risk_score: riskScore,
                target_response_seconds: targetSeconds,
                ai_summary: `${requestType} / ${urgency} Assistance`,
                ai_explanation: explanation
            });

            setCreatedRequest({
                ...req,
                language: selectedLanguage.name,
                urgency,
                risk_score: riskScore,
                target_response_window: `${String(Math.floor(targetSeconds / 60)).padStart(2, '0')}:${String(targetSeconds % 60).padStart(2, '0')}`,
                explanation,
                caretakerNotified: true
            });

            setStep('complete');
        }, 1500);
    };

    return (
        <div className="max-w-2xl mx-auto space-y-6 pb-24 pt-2 animate-fade-in">
            
            {/* Back button */}
            <div>
                <button 
                    onClick={() => navigate('/senior')}
                    className="inline-flex items-center text-sm font-semibold text-slate-500 hover:text-sky-600 transition-colors"
                >
                    <ArrowLeft className="w-4 h-4 mr-1.5" /> Back to Dashboard
                </button>
            </div>

            <div className="text-center">
                <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                    Tell NEARHAND what you need.
                </h1>
                <p className="text-base text-slate-600 mt-1.5 font-medium">
                    Speak naturally in your preferred language or type below.
                </p>
            </div>

            {/* Language Selector (Part 7) */}
            <Card className="p-4 sm:p-5 border-slate-200">
                <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center">
                        <Globe2 className="w-4 h-4 mr-1.5 text-sky-600" /> Select Language
                    </span>
                    <span className="text-xs font-semibold text-sky-600">
                        Speech recognition configured for: {selectedLanguage.name} ({selectedLanguage.code})
                    </span>
                </div>

                <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
                    {LANGUAGES.map(lang => (
                        <button
                            key={lang.code}
                            onClick={() => {
                                if (isListening) stopListening();
                                setSelectedLanguage(lang);
                            }}
                            className={`py-2 px-2.5 rounded-xl text-center border font-bold text-xs transition-all ${
                                selectedLanguage.code === lang.code
                                    ? 'bg-sky-600 text-white border-sky-600 shadow-xs scale-102'
                                    : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
                            }`}
                        >
                            <span className="block text-sm leading-tight">{lang.nativeName}</span>
                            <span className="block text-[10px] opacity-80 mt-0.5">{lang.name}</span>
                        </button>
                    ))}
                </div>
            </Card>

            {step === 'input' && (
                <div className="space-y-6">
                    
                    {/* Browser Speech Recognition Warning if Unsupported */}
                    {!isSupported && (
                        <div className="p-4 bg-amber-50 border border-amber-200 rounded-2xl text-amber-800 text-sm flex items-start space-x-3">
                            <AlertCircle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                            <div>
                                <p className="font-bold">Voice input isn't supported in this browser.</p>
                                <p className="text-xs mt-0.5 text-amber-700">
                                    You can type your request in the field below or click a sample phrase.
                                </p>
                            </div>
                        </div>
                    )}

                    {speechError && (
                        <div className="p-4 bg-rose-50 border border-rose-200 rounded-2xl text-rose-800 text-sm flex items-center space-x-3">
                            <AlertCircle className="w-5 h-5 text-rose-600 shrink-0" />
                            <p className="text-xs font-semibold">{speechError}</p>
                        </div>
                    )}

                    {/* Microphone Section (Part 6) */}
                    <Card className="p-8 text-center border-2 border-slate-200 flex flex-col items-center justify-center">
                        {isListening ? (
                            <div className="space-y-4 flex flex-col items-center">
                                <div className="w-28 h-28 bg-rose-50 text-rose-600 rounded-full flex items-center justify-center border-4 border-rose-200 shadow-xl animate-listening">
                                    <Mic className="w-12 h-12 text-rose-600 animate-pulse" />
                                </div>
                                <div className="flex items-center space-x-2">
                                    <span className="w-3 h-3 rounded-full bg-rose-500 animate-ping"></span>
                                    <span className="text-lg font-black text-rose-600">🔴 Listening...</span>
                                    <span className="font-mono text-base font-bold bg-slate-100 text-slate-800 px-2.5 py-0.5 rounded-lg ml-2">
                                        {formattedDuration}
                                    </span>
                                </div>
                                <Button 
                                    variant="secondary"
                                    onClick={handleStopRecording}
                                    className="border-rose-200 text-rose-700 hover:bg-rose-50 font-bold px-6 py-2.5 rounded-xl"
                                >
                                    <Square className="w-4 h-4 mr-2 text-rose-600" /> Stop Recording
                                </Button>
                            </div>
                        ) : (
                            <div className="space-y-4 flex flex-col items-center">
                                <button
                                    onClick={handleStartRecording}
                                    className="w-28 h-28 bg-sky-50 hover:bg-sky-100 text-sky-600 rounded-full flex items-center justify-center border-4 border-sky-200 hover:border-sky-400 shadow-xl transition-all transform hover:scale-105 active:scale-95 cursor-pointer group"
                                    title="Click to speak your request"
                                >
                                    <Mic className="w-12 h-12 text-sky-600 group-hover:scale-110 transition-transform" />
                                </button>
                                <div>
                                    <p className="font-extrabold text-xl text-slate-900">🎙 Speak your request</p>
                                    <p className="text-xs text-slate-500 mt-1 font-medium">
                                        Microphone will listen in <span className="font-bold text-sky-700">{selectedLanguage.name}</span>
                                    </p>
                                </div>
                            </div>
                        )}

                        {/* Live interim transcript stream */}
                        {interimTranscript && (
                            <div className="mt-4 p-3 bg-sky-50/70 border border-sky-100 rounded-xl text-slate-700 text-sm italic font-medium w-full text-center">
                                "...{interimTranscript}"
                            </div>
                        )}
                    </Card>

                    {/* Quick Demo Sample Preset */}
                    <div className="flex items-center justify-between text-xs px-1">
                        <span className="font-bold text-slate-400 uppercase tracking-wider">
                            Demo Shortcut:
                        </span>
                        <button
                            onClick={() => handlePresetClick(selectedLanguage.sample)}
                            className="font-bold text-sky-600 hover:text-sky-800 underline cursor-pointer"
                        >
                            Fill "{selectedLanguage.sample}"
                        </button>
                    </div>

                    {/* Editable Transcript Textarea */}
                    <Card className="p-5 border-slate-200 space-y-3">
                        <div className="flex items-center justify-between">
                            <label className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center">
                                <Keyboard className="w-4 h-4 mr-1.5 text-slate-400" /> Transcript / Text Request
                            </label>
                            {textInput && (
                                <span className="text-xs font-bold text-emerald-600 flex items-center">
                                    <CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Transcript ready ✓
                                </span>
                            )}
                        </div>

                        <textarea
                            value={textInput}
                            onChange={(e) => setTextInput(e.target.value)}
                            rows={3}
                            placeholder="Your spoken words will appear here, or you can type directly..."
                            className="w-full p-4 rounded-2xl border border-slate-200 focus:border-sky-500 focus:ring-2 focus:ring-sky-500/20 text-base text-slate-800 outline-none resize-none transition-colors"
                        />

                        <div className="flex justify-between items-center pt-2">
                            <button
                                onClick={() => {
                                    resetTranscript();
                                    setTextInput('');
                                }}
                                className="text-xs text-slate-400 hover:text-slate-600 flex items-center"
                            >
                                <RotateCcw className="w-3.5 h-3.5 mr-1" /> Clear
                            </button>

                            <Button
                                size="lg"
                                disabled={!textInput.trim()}
                                onClick={handleSubmit}
                                className="px-8 font-bold rounded-2xl shadow-md bg-sky-600 hover:bg-sky-700"
                            >
                                <Send className="w-4 h-4 mr-2" /> Submit Request
                            </Button>
                        </div>
                    </Card>

                </div>
            )}

            {/* Analyzing State */}
            {step === 'analyzing' && (
                <Card className="p-16 text-center border-slate-200 space-y-6">
                    <div className="relative w-24 h-24 mx-auto">
                        <div className="w-24 h-24 rounded-full bg-sky-50 border-4 border-sky-100 flex items-center justify-center animate-pulse">
                            <Sparkles className="w-10 h-10 text-sky-600 animate-spin-slow" />
                        </div>
                        <div className="absolute inset-0 rounded-full border-4 border-sky-400 animate-ping opacity-30"></div>
                    </div>
                    <div>
                        <h3 className="text-2xl font-bold text-slate-900">Understanding your request...</h3>
                        <p className="text-sm text-slate-500 mt-1">
                            Analyzing urgency, language signals, and determining response pathway...
                        </p>
                    </div>
                </Card>
            )}

            {/* Complete / AI Analysis View (Part 13) */}
            {step === 'complete' && createdRequest && (
                <div className="space-y-6">
                    <AIAnalysisCard
                        analysis={createdRequest}
                        onProceed={() => navigate(`/request/${createdRequest.id}`)}
                        proceedLabel="View Live Response Monitor →"
                    />
                </div>
            )}

        </div>
    );
}
