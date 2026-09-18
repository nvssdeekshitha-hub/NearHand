import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
    ShieldPlus, 
    MapPin, 
    CheckCircle2, 
    Clock, 
    Lock, 
    Unlock, 
    Phone, 
    AlertTriangle,
    HeartHandshake
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { useAuth } from '../../context/AuthContext';
import { useCare } from '../../context/CareContext';

export function VolunteerDashboard() {
    const navigate = useNavigate();
    const { user } = useAuth();
    const { 
        volunteerEligibleRequests, 
        volunteerActiveAssistance, 
        volunteerAccept, 
        resolveRequest 
    } = useCare();

    const [isAvailable, setIsAvailable] = useState(true);
    const [callModal, setCallModal] = useState(null);

    const handleAccept = async (requestId) => {
        await volunteerAccept(requestId);
    };

    const handleResolve = async (requestId) => {
        await resolveRequest(requestId, 'Volunteer Priya Sharma provided first-aid assistance and ensured safe transfer.');
    };

    return (
        <div className="max-w-4xl mx-auto space-y-8 pb-20 animate-fade-in">
            
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-200">
                <div>
                    <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                        Nearby Assistance Network
                    </h1>
                    <p className="text-slate-500 font-medium text-sm mt-1">
                        Welcome, {user?.name || 'Priya Sharma'} • First-Aid & CPR Certified
                    </p>
                </div>

                <div className="flex items-center space-x-3">
                    <button
                        onClick={() => setIsAvailable(!isAvailable)}
                        className={`flex items-center space-x-2 px-4 py-2 rounded-full border text-xs font-bold transition-colors ${
                            isAvailable
                                ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                                : 'bg-slate-100 text-slate-600 border-slate-200'
                        }`}
                    >
                        <span className={`w-2.5 h-2.5 rounded-full ${isAvailable ? 'bg-emerald-500 animate-ping' : 'bg-slate-400'}`} />
                        <span>{isAvailable ? '🟢 Available' : '⚪ Busy / Offline'}</span>
                    </button>
                    <span className="text-xs font-semibold text-slate-500 flex items-center bg-white px-3 py-1.5 rounded-xl border border-slate-200">
                        <MapPin className="w-3.5 h-3.5 mr-1 text-sky-600" /> Sharing GPS
                    </span>
                </div>
            </div>

            {/* Volunteer Community Context Banner */}
            <div className="bg-sky-50 border border-sky-200 p-4 sm:p-5 rounded-2xl flex items-start space-x-3 shadow-xs">
                <ShieldPlus className="w-6 h-6 text-sky-700 shrink-0 mt-0.5" />
                <div className="text-xs text-slate-700 leading-relaxed">
                    <strong className="text-slate-900 font-bold block mb-0.5">Independent Community Responder Protocol:</strong>
                    You are enrolled as an independent community volunteer. Requests appear here <strong className="text-slate-900">only</strong> when a primary caretaker response window has expired or immediate backup was explicitly escalated. Full personal contact info remains privacy-locked until you accept.
                </div>
            </div>

            {/* Section 1: MY ACTIVE ASSISTANCE (Part 18) */}
            {volunteerActiveAssistance.length > 0 && (
                <div className="space-y-4">
                    <div className="flex items-center space-x-2">
                        <HeartHandshake className="w-5 h-5 text-emerald-600" />
                        <h2 className="text-xl font-bold text-slate-900">My Active Assistance</h2>
                        <Badge variant="success">In Progress</Badge>
                    </div>

                    {volunteerActiveAssistance.map(req => (
                        <Card key={req.id} className="p-6 border-2 border-emerald-300 bg-emerald-50/20 shadow-md">
                            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                                <div className="space-y-2">
                                    <div className="flex items-center space-x-3">
                                        <h3 className="text-2xl font-black text-slate-900">{req.senior_name}, {req.senior_age}</h3>
                                        <Badge variant="critical">CRITICAL</Badge>
                                        <span className="text-xs bg-emerald-100 text-emerald-800 font-bold px-2.5 py-0.5 rounded-full flex items-center">
                                            <Unlock className="w-3 h-3 mr-1" /> Contact Unlocked
                                        </span>
                                    </div>
                                    <p className="text-base font-bold text-slate-800">{req.ai_summary}</p>
                                    
                                    <div className="bg-white p-3 rounded-xl border border-emerald-200 text-xs space-y-1 mt-2">
                                        <p className="text-slate-800 font-semibold flex items-center">
                                            <MapPin className="w-3.5 h-3.5 mr-1.5 text-rose-600" /> {req.location} (Plot 42, Moghalrajpuram)
                                        </p>
                                        <p className="text-slate-600">
                                            Family Contact: Anjali (+91 98480 11223) • Caretaker: Ravi Kumar (+91 98765 43210)
                                        </p>
                                    </div>
                                </div>

                                <div className="flex flex-col gap-2.5 w-full md:w-56 shrink-0">
                                    <Button 
                                        variant="success" 
                                        size="lg"
                                        className="w-full font-bold shadow-md"
                                        onClick={() => handleResolve(req.id)}
                                    >
                                        Resolve Request ✓
                                    </Button>
                                    <Button 
                                        variant="secondary"
                                        className="w-full text-xs font-semibold"
                                        onClick={() => setCallModal({ name: `Lakshmi / Family Anjali`, phone: '+91 98480 11223' })}
                                    >
                                        <Phone className="w-3.5 h-3.5 mr-1.5 text-sky-600" /> Call Family / Caretaker
                                    </Button>
                                </div>
                            </div>
                        </Card>
                    ))}
                </div>
            )}

            {/* Section 2: NEARBY ASSISTANCE QUEUE */}
            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                        <AlertTriangle className="w-5 h-5 text-amber-500" />
                        <h2 className="text-xl font-bold text-slate-900">Nearby Escalated Requests</h2>
                    </div>
                    <Badge variant="warning">{volunteerEligibleRequests.length} Available</Badge>
                </div>

                {volunteerEligibleRequests.length === 0 ? (
                    <Card className="p-12 text-center border-dashed border-2 border-slate-200">
                        <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto mb-3 opacity-80" />
                        <h3 className="text-lg font-bold text-slate-800">You're all caught up</h3>
                        <p className="text-sm text-slate-500 mt-1">
                            No escalated requests currently require community volunteer assistance.
                        </p>
                    </Card>
                ) : (
                    <div className="space-y-4">
                        {volunteerEligibleRequests.map(req => (
                            <Card 
                                key={req.id} 
                                className="p-0 overflow-hidden border-2 border-rose-200 shadow-lg relative"
                            >
                                <div className="p-6 pl-8">
                                    <div className="flex flex-col md:flex-row md:items-start justify-between gap-6">
                                        
                                        {/* Minimum Necessary Information (Privacy Principle) */}
                                        <div className="space-y-3 flex-1">
                                            <div className="flex flex-wrap items-center gap-3">
                                                <h3 className="text-2xl font-black text-slate-900">{req.senior_name}</h3>
                                                <Badge variant="critical">CRITICAL</Badge>
                                                <span className="text-xs bg-slate-100 text-slate-700 font-bold px-3 py-1 rounded-full flex items-center border border-slate-200">
                                                    <MapPin className="w-3.5 h-3.5 mr-1 text-sky-600" /> 2.4 km away
                                                </span>
                                                <span className="text-xs bg-emerald-50 text-emerald-800 font-semibold px-2.5 py-1 rounded-full border border-emerald-200">
                                                    First-Aid Matched
                                                </span>
                                            </div>

                                            <p className="text-lg font-bold text-slate-800">
                                                Situation: {req.ai_summary || 'Fall assistance required'}
                                            </p>

                                            <div className="flex items-center space-x-6 text-xs text-slate-500 font-medium">
                                                <span className="flex items-center font-bold text-sky-700">
                                                    <Clock className="w-4 h-4 mr-1 text-sky-600" /> ETA: ~7 min
                                                </span>
                                                <span>•</span>
                                                <span className="text-rose-600 font-semibold">
                                                    Reason: Caretaker timeout
                                                </span>
                                            </div>
                                        </div>

                                        {/* Accept Button */}
                                        <div className="flex flex-col space-y-2.5 w-full md:w-56 shrink-0">
                                            <Button 
                                                variant="emergency" 
                                                size="lg"
                                                onClick={() => handleAccept(req.id)}
                                                className="w-full text-base font-bold py-4 rounded-2xl shadow-rose-600/30"
                                            >
                                                Accept Request
                                            </Button>
                                            <Button 
                                                variant="secondary" 
                                                className="w-full text-xs"
                                                onClick={() => navigate(`/request/${req.id}`)}
                                            >
                                                View Request Details
                                            </Button>
                                        </div>
                                    </div>

                                    {/* Privacy Lock Banner (Part 19) */}
                                    <div className="mt-6 pt-3.5 border-t border-slate-100 -mx-6 -mb-6 p-4 px-8 bg-amber-50/70 flex items-start space-x-3 text-xs">
                                        <Lock className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
                                        <p className="text-slate-600 leading-relaxed">
                                            <strong className="text-amber-900 uppercase tracking-wider font-bold">Privacy Lock:</strong> For senior safety and data privacy, specific street address and family contact numbers remain protected until you formally click <strong>Accept Request</strong>.
                                        </p>
                                    </div>
                                </div>
                            </Card>
                        ))}
                    </div>
                )}
            </div>

            {/* Direct Call Modal */}
            {callModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4 animate-fade-in">
                    <Card className="max-w-sm w-full p-6 text-center">
                        <Phone className="w-12 h-12 text-sky-600 mx-auto mb-3" />
                        <h3 className="font-bold text-lg text-slate-900 mb-1">{callModal.name}</h3>
                        <p className="text-slate-600 text-sm mb-6">{callModal.phone}</p>
                        <Button className="w-full font-bold" onClick={() => setCallModal(null)}>Close</Button>
                    </Card>
                </div>
            )}

        </div>
    );
}
