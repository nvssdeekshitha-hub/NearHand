import React from 'react';
import { Clock, AlertTriangle, ShieldCheck } from 'lucide-react';

export function ResponseTimer({ 
    secondsRemaining, 
    totalSeconds = 120 
}) {
    const isExpired = secondsRemaining <= 0;
    const minutes = Math.floor(Math.max(0, secondsRemaining) / 60);
    const seconds = Math.max(0, secondsRemaining) % 60;
    const formatted = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    const percent = Math.min(100, Math.max(0, (secondsRemaining / totalSeconds) * 100));

    return (
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
            <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2 text-slate-500 text-xs font-bold uppercase tracking-wider">
                    <Clock className="w-4 h-4 text-sky-600" />
                    <span>Target Response Window</span>
                </div>
                <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full ${
                    isExpired ? 'bg-rose-100 text-rose-700' : 'bg-sky-50 text-sky-700'
                }`}>
                    {isExpired ? 'Window Expired' : 'Active Countdown'}
                </span>
            </div>

            <div className="flex items-baseline space-x-3 mb-2">
                <span className={`font-mono text-3xl md:text-4xl font-black ${
                    isExpired ? 'text-rose-600' : secondsRemaining < 30 ? 'text-amber-500 animate-pulse' : 'text-slate-900'
                }`}>
                    {formatted}
                </span>
                <span className="text-xs text-slate-400 font-medium">
                    {isExpired ? 'Overdue' : 'remaining'}
                </span>
            </div>

            {/* Progress bar */}
            <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden mb-3">
                <div 
                    className={`h-full transition-all duration-1000 ${
                        isExpired ? 'bg-rose-500' : secondsRemaining < 30 ? 'bg-amber-500' : 'bg-sky-500'
                    }`}
                    style={{ width: `${percent}%` }}
                />
            </div>

            <div className="text-xs text-slate-500 font-medium flex items-center">
                {isExpired ? (
                    <span className="text-rose-600 font-semibold flex items-center">
                        <AlertTriangle className="w-3.5 h-3.5 mr-1.5" /> Caretaker response window expired. Escalating to nearby support...
                    </span>
                ) : (
                    <span className="flex items-center">
                        <ShieldCheck className="w-3.5 h-3.5 mr-1.5 text-emerald-500" /> Waiting for primary caretaker acknowledgement
                    </span>
                )}
            </div>
        </div>
    );
}
