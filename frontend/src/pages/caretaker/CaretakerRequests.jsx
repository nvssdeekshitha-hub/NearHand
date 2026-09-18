import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
    Clock, 
    CheckCircle2, 
    ArrowLeft, 
    MapPin, 
    Activity
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { useCare } from '../../context/CareContext';

export function CaretakerRequests() {
    const navigate = useNavigate();
    const { activeRequests, caretakerAccept, caretakerTimeout, resolveRequest } = useCare();
    const [filter, setFilter] = useState('all'); // all | critical | waiting | in_progress

    const filtered = activeRequests.filter(req => {
        if (filter === 'critical') return req.urgency === 'CRITICAL';
        if (filter === 'waiting') return req.status === 'WAITING_FOR_RESPONSE' || req.status === 'CARETAKER_NOTIFIED';
        if (filter === 'in_progress') return req.status === 'ACCEPTED' || req.status === 'IN_PROGRESS';
        return true;
    });

    return (
        <div className="max-w-5xl mx-auto space-y-6 pb-20 animate-fade-in">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
                <div>
                    <button 
                        onClick={() => navigate('/caretaker')}
                        className="text-xs font-bold text-slate-500 hover:text-sky-600 flex items-center mb-2"
                    >
                        <ArrowLeft className="w-3.5 h-3.5 mr-1" /> Back to Dashboard
                    </button>
                    <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
                        Active Requests Queue
                    </h1>
                </div>

                {/* Filter Pills */}
                <div className="flex flex-wrap gap-2">
                    {[
                        { id: 'all', label: `All (${activeRequests.length})` },
                        { id: 'critical', label: 'Critical' },
                        { id: 'waiting', label: 'Awaiting Response' },
                        { id: 'in_progress', label: 'In Progress' }
                    ].map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setFilter(tab.id)}
                            className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-colors ${
                                filter === tab.id
                                    ? 'bg-sky-600 text-white shadow-xs'
                                    : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
                            }`}
                        >
                            {tab.label}
                        </button>
                    ))}
                </div>
            </div>

            {/* Requests List */}
            {filtered.length === 0 ? (
                <Card className="p-16 text-center border-dashed border-2 border-slate-200">
                    <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto mb-3" />
                    <h3 className="text-lg font-bold text-slate-800">No matching requests</h3>
                    <p className="text-sm text-slate-500 mt-1">There are no active requests in this filter.</p>
                </Card>
            ) : (
                <div className="space-y-4">
                    {filtered.map(req => {
                        const isCritical = req.urgency === 'CRITICAL';
                        const isWaiting = req.status === 'WAITING_FOR_RESPONSE' || req.status === 'CARETAKER_NOTIFIED';

                        const minutes = Math.floor((req.seconds_remaining || 0) / 60);
                        const seconds = (req.seconds_remaining || 0) % 60;
                        const timerStr = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

                        return (
                            <Card key={req.id} className="p-6 border-slate-200 shadow-sm hover:border-slate-300 transition-all">
                                <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                                    <div className="space-y-2 flex-1">
                                        <div className="flex items-center space-x-3">
                                            <h3 className="text-2xl font-black text-slate-900">
                                                {req.senior_name}, {req.senior_age}
                                            </h3>
                                            <Badge variant={isCritical ? 'critical' : 'warning'}>
                                                {req.urgency}
                                            </Badge>
                                            <span className="text-xs text-slate-500 font-mono font-bold">
                                                #{req.id}
                                            </span>
                                        </div>

                                        <p className="text-base font-bold text-slate-800">
                                            {req.ai_summary}
                                        </p>

                                        {req.original_transcript && (
                                            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs text-slate-700 italic">
                                                "{req.original_transcript}"
                                            </div>
                                        )}

                                        <div className="flex flex-wrap gap-4 text-xs text-slate-500 pt-1">
                                            <span className="flex items-center">
                                                <MapPin className="w-3.5 h-3.5 mr-1 text-slate-400" /> {req.location}
                                            </span>
                                            <span className="flex items-center">
                                                <Activity className="w-3.5 h-3.5 mr-1 text-slate-400" /> Priority: {req.risk_score}/100
                                            </span>
                                            <span className="flex items-center">
                                                <Clock className="w-3.5 h-3.5 mr-1 text-slate-400" /> Status: {req.status}
                                            </span>
                                        </div>
                                    </div>

                                    {/* Right Action Panel */}
                                    <div className="flex flex-col gap-2.5 w-full md:w-56 shrink-0 pt-2 md:pt-0">
                                        {isWaiting && (
                                            <div className="bg-rose-50 border border-rose-200 p-2.5 rounded-xl text-center text-xs font-mono font-bold text-rose-700">
                                                ⏱ {timerStr} remaining
                                            </div>
                                        )}

                                        {isWaiting && (
                                            <Button 
                                                variant="emergency" 
                                                className="w-full font-bold"
                                                onClick={() => caretakerAccept(req.id)}
                                            >
                                                Accept Request
                                            </Button>
                                        )}

                                        <Button 
                                            variant="success" 
                                            className="w-full font-bold"
                                            onClick={() => resolveRequest(req.id, 'Resolved by Caretaker.')}
                                        >
                                            Mark Resolved
                                        </Button>

                                        <Button 
                                            variant="secondary" 
                                            className="w-full"
                                            onClick={() => navigate(`/request/${req.id}`)}
                                        >
                                            View Monitor
                                        </Button>

                                        {isWaiting && (
                                            <button
                                                onClick={() => caretakerTimeout(req.id)}
                                                className="text-[11px] text-slate-400 hover:text-amber-600 underline text-center pt-1"
                                            >
                                                Trigger Timeout / Escalate
                                            </button>
                                        )}
                                    </div>
                                </div>
                            </Card>
                        );
                    })}
                </div>
            )}
        </div>
    );
}
