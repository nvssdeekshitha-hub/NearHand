import React from 'react';
import { Sparkles, Clock, Info, CheckCircle2 } from 'lucide-react';
import { Badge } from '../ui/Badge';
import { Card } from '../ui/Card';

export function AIAnalysisCard({ analysis, onProceed, proceedLabel = "Continue to Live Monitor" }) {
    if (!analysis) return null;

    const {
        language = 'Telugu',
        request_type = 'Fall',
        urgency = 'CRITICAL',
        risk_score = 94,
        target_response_window = '02:00',
        explanation = 'The request indicates a sudden fall and immediate inability to stand up. High risk of injury or hip fracture.',
        caretakerNotified = true
    } = analysis;

    const isCritical = urgency === 'CRITICAL';
    const isWarning = urgency === 'WARNING';

    return (
        <Card className="p-6 md:p-8 border-2 border-sky-200 shadow-xl bg-white rounded-3xl relative overflow-hidden animate-fade-in">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-6">
                <div className="flex items-center space-x-2.5 text-sky-700">
                    <div className="w-9 h-9 rounded-xl bg-sky-50 flex items-center justify-center border border-sky-100">
                        <Sparkles className="w-5 h-5 text-sky-600 animate-pulse" />
                    </div>
                    <div>
                        <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Analysis Engine</span>
                        <h3 className="text-lg font-extrabold text-slate-900 leading-tight">✨ NEARHAND AI</h3>
                    </div>
                </div>
                <Badge variant={isCritical ? 'critical' : isWarning ? 'warning' : 'primary'} className="text-xs px-3 py-1">
                    {urgency}
                </Badge>
            </div>

            {/* Content Fields */}
            <div className="space-y-4 text-sm">
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div className="bg-slate-50 p-3.5 rounded-2xl border border-slate-100">
                        <p className="text-[11px] font-bold uppercase text-slate-400">Language</p>
                        <p className="font-bold text-slate-900 text-base mt-0.5">{language}</p>
                    </div>
                    <div className="bg-slate-50 p-3.5 rounded-2xl border border-slate-100">
                        <p className="text-[11px] font-bold uppercase text-slate-400">Request Type</p>
                        <p className="font-bold text-slate-900 text-base mt-0.5">{request_type}</p>
                    </div>
                    <div className="bg-slate-50 p-3.5 rounded-2xl border border-slate-100">
                        <p className="text-[11px] font-bold uppercase text-slate-400">Priority Score</p>
                        <p className={`font-black text-lg mt-0.5 ${risk_score >= 85 ? 'text-rose-600' : risk_score >= 60 ? 'text-amber-600' : 'text-sky-600'}`}>
                            {risk_score} / 100
                        </p>
                    </div>
                    <div className="bg-sky-50 p-3.5 rounded-2xl border border-sky-100">
                        <p className="text-[11px] font-bold uppercase text-sky-600 flex items-center">
                            <Clock className="w-3.5 h-3.5 mr-1" /> Target Window
                        </p>
                        <p className="font-mono font-black text-lg text-sky-700 mt-0.5">
                            {target_response_window}
                        </p>
                    </div>
                </div>

                {/* AI Explanation */}
                <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100">
                    <p className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1 flex items-center">
                        <Info className="w-3.5 h-3.5 mr-1 text-sky-500" /> AI-Assisted Assessment
                    </p>
                    <p className="text-slate-700 font-medium leading-relaxed">
                        "{explanation}"
                    </p>
                    <p className="text-[11px] text-slate-400 mt-2 italic">
                        *AI-assisted coordination target, not a medical diagnosis or safety guarantee.
                    </p>
                </div>

                {/* Caretaker Notification Status */}
                {caretakerNotified && (
                    <div className="flex items-center justify-between bg-emerald-50 border border-emerald-200 p-3.5 rounded-2xl text-emerald-800 font-bold">
                        <div className="flex items-center">
                            <CheckCircle2 className="w-5 h-5 mr-2.5 text-emerald-600" />
                            <span>Primary Caretaker Notified (Ravi Kumar)</span>
                        </div>
                        <span className="text-xs bg-emerald-100 text-emerald-800 px-2.5 py-0.5 rounded-full">
                            Active
                        </span>
                    </div>
                )}
            </div>

            {onProceed && (
                <button
                    onClick={onProceed}
                    className="w-full mt-6 py-3.5 bg-slate-900 hover:bg-slate-800 text-white font-bold text-base rounded-2xl transition-all shadow-md active:scale-[0.99]"
                >
                    {proceedLabel}
                </button>
            )}
        </Card>
    );
}
