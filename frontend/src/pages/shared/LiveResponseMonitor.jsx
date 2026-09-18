import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
    ShieldAlert, 
    CheckCircle2, 
    Clock, 
    AlertTriangle, 
    UserCheck, 
    ShieldPlus, 
    ArrowLeft, 
    MapPin, 
    Phone,
    HeartHandshake
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { ResponseTimer } from '../../components/ai/ResponseTimer';
import { useCare } from '../../context/CareContext';

export function LiveResponseMonitor() {
    const { id } = useParams();
    const navigate = useNavigate();
    const { 
        requests, 
        caretakerTimeout, 
        volunteerAccept, 
        resolveRequest 
    } = useCare();

    // Look for matching request or default to active Lakshmi request
    const request = requests.find(r => r.id === id) || requests.find(r => r.senior_name === 'Lakshmi') || requests[0];

    if (!request) {
        return (
            <div className="max-w-2xl mx-auto py-20 text-center">
                <p className="text-slate-500">Request not found.</p>
                <Button onClick={() => navigate('/caretaker')} className="mt-4">Return to Dashboard</Button>
            </div>
        );
    }

    const isWaiting = request.status === 'WAITING_FOR_RESPONSE' || request.status === 'CARETAKER_NOTIFIED';
    const isEscalated = request.status === 'ESCALATED';
    const isVolunteerAccepted = request.status === 'IN_PROGRESS' || Boolean(request.assigned_volunteer_name);
    const isResolved = request.status === 'RESOLVED';

    // Current step calculation
    let currentStep = 1;
    if (isWaiting) currentStep = 2;
    if (isEscalated) currentStep = 3;
    if (isVolunteerAccepted) currentStep = 5;
    if (isResolved) currentStep = 6;

    return (
        <div className="max-w-4xl mx-auto py-6 space-y-6 animate-fade-in">
            {/* Header */}
            <div className="flex items-center justify-between pb-4 border-b border-slate-200">
                <button
                    onClick={() => navigate(-1)}
                    className="inline-flex items-center text-xs font-bold text-slate-500 hover:text-sky-600 transition-colors"
                >
                    <ArrowLeft className="w-3.5 h-3.5 mr-1" /> Back
                </button>
                <Badge variant={request.urgency === 'CRITICAL' ? 'critical' : 'warning'}>
                    {request.urgency}
                </Badge>
            </div>

            <div className="text-center">
                <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                    NEARHAND Live Response Monitor
                </h1>
                <p className="text-slate-500 mt-1 font-medium text-sm">
                    Tracking Incident #{request.id} for <strong className="text-slate-900">{request.senior_name}</strong> ({request.senior_age})
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* Event Timeline */}
                <Card className="p-6 md:p-8">
                    <h2 className="text-lg font-bold text-slate-900 mb-6 border-b border-slate-100 pb-3">
                        Incident Progression Timeline
                    </h2>

                    <div className="relative border-l-2 border-slate-200 ml-3 space-y-6 text-xs">
                        
                        {/* 1: Analyzed */}
                        <div className="relative pl-6">
                            <span className="absolute -left-[17px] top-0 bg-emerald-500 text-white rounded-full p-1 border-4 border-white">
                                <CheckCircle2 className="w-3.5 h-3.5" />
                            </span>
                            <h4 className="font-bold text-sm text-slate-900">Request Captured & AI Analyzed</h4>
                            <p className="text-slate-500 mt-0.5">Priority: {request.risk_score}/100 • {request.ai_summary}</p>
                        </div>

                        {/* 2: Caretaker Notified */}
                        <div className="relative pl-6">
                            <span className={`absolute -left-[17px] top-0 rounded-full p-1 border-4 border-white ${
                                currentStep >= 2 ? 'bg-sky-500 text-white' : 'bg-slate-200'
                            }`}>
                                <Clock className="w-3.5 h-3.5" />
                            </span>
                            <h4 className={`font-bold text-sm ${currentStep >= 2 ? 'text-slate-900' : 'text-slate-400'}`}>
                                Caretaker Notification Dispatched
                            </h4>
                            <p className="text-slate-500 mt-0.5">Assigned to primary: Ravi Kumar</p>
                            {isWaiting && (
                                <p className="text-amber-600 font-bold mt-1">Awaiting caretaker response...</p>
                            )}
                            {currentStep > 2 && (
                                <p className="text-rose-600 font-semibold mt-1">Caretaker did not acknowledge in time</p>
                            )}
                        </div>

                        {/* 3: Escalation */}
                        <div className="relative pl-6">
                            <span className={`absolute -left-[17px] top-0 rounded-full p-1 border-4 border-white ${
                                currentStep >= 3 ? 'bg-amber-500 text-white' : 'bg-slate-200'
                            }`}>
                                <AlertTriangle className="w-3.5 h-3.5" />
                            </span>
                            <h4 className={`font-bold text-sm ${currentStep >= 3 ? 'text-slate-900' : 'text-slate-400'}`}>
                                Community Volunteer Escalation
                            </h4>
                            {isEscalated && (
                                <p className="text-sky-600 font-bold mt-1">Searching nearby available volunteers within 5 km...</p>
                            )}
                            {currentStep >= 5 && (
                                <p className="text-emerald-700 font-bold mt-1">Volunteer Priya Sharma accepted the request</p>
                            )}
                        </div>

                        {/* 4: Family Notification */}
                        <div className="relative pl-6">
                            <span className={`absolute -left-[17px] top-0 rounded-full p-1 border-4 border-white ${
                                currentStep >= 5 ? 'bg-emerald-500 text-white' : 'bg-slate-200'
                            }`}>
                                <CheckCircle2 className="w-3.5 h-3.5" />
                            </span>
                            <h4 className={`font-bold text-sm ${currentStep >= 5 ? 'text-slate-900' : 'text-slate-400'}`}>
                                Family Notified of Responder Dispatch
                            </h4>
                            <p className="text-slate-500 mt-0.5">Real-time alert pushed to Anjali</p>
                        </div>

                        {/* 5: Resolution */}
                        <div className="relative pl-6">
                            <span className={`absolute -left-[17px] top-0 rounded-full p-1 border-4 border-white ${
                                isResolved ? 'bg-emerald-600 text-white' : 'bg-slate-200'
                            }`}>
                                <CheckCircle2 className="w-3.5 h-3.5" />
                            </span>
                            <h4 className={`font-bold text-sm ${isResolved ? 'text-slate-900' : 'text-slate-400'}`}>
                                Incident Resolved
                            </h4>
                            <p className="text-slate-500 mt-0.5">
                                {isResolved ? request.resolution_notes : 'Awaiting physical on-scene verification'}
                            </p>
                        </div>

                    </div>
                </Card>

                {/* Right Panel: Dynamic Status Card */}
                <div className="space-y-4">
                    
                    {/* Active Timer or Escalation Card */}
                    {isWaiting && (
                        <div className="space-y-4">
                            <ResponseTimer
                                secondsRemaining={request.seconds_remaining}
                                totalSeconds={request.target_response_seconds}
                                onTimeout={() => caretakerTimeout(request.id)}
                            />

                            <Card className="p-5 border-amber-200 bg-amber-50/50">
                                <h4 className="font-bold text-amber-900 text-sm mb-1">Caretaker Action Needed</h4>
                                <p className="text-xs text-slate-600 mb-4">
                                    Primary caretaker has not yet acknowledged. If no action occurs before the timer elapses, NEARHAND will activate nearby volunteers.
                                </p>
                                <Button 
                                    size="sm"
                                    className="w-full bg-amber-600 hover:bg-amber-700 text-white font-bold"
                                    onClick={() => caretakerTimeout(request.id)}
                                >
                                    Simulate No Response (Force Escalation)
                                </Button>
                            </Card>
                        </div>
                    )}

                    {isEscalated && (
                        <Card className="p-6 border-2 border-amber-300 bg-amber-50/30 text-center space-y-4">
                            <div className="w-16 h-16 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center mx-auto animate-pulse">
                                <AlertTriangle className="w-8 h-8" />
                            </div>
                            <div>
                                <h3 className="text-xl font-bold text-amber-950">Caretaker Timeout Occurred</h3>
                                <p className="text-xs text-slate-600 mt-1">
                                    Automatic fallback initiated. Matching nearby certified community volunteers...
                                </p>
                            </div>

                            <div className="bg-white p-4 rounded-2xl border border-slate-200 text-left space-y-2">
                                <div className="flex items-center justify-between">
                                    <h4 className="font-bold text-slate-900 text-sm">Priya Sharma</h4>
                                    <Badge variant="teal">First-Aid Trained</Badge>
                                </div>
                                <p className="text-xs text-slate-500">📍 2.4 km away • ETA: ~7 mins</p>
                                <Button 
                                    size="sm" 
                                    variant="emergency" 
                                    className="w-full font-bold mt-2"
                                    onClick={() => volunteerAccept(request.id)}
                                >
                                    Accept as Volunteer Priya
                                </Button>
                            </div>
                        </Card>
                    )}

                    {isVolunteerAccepted && !isResolved && (
                        <Card className="p-6 border-2 border-emerald-300 bg-emerald-50/30 space-y-4">
                            <div className="w-14 h-14 bg-emerald-100 text-emerald-700 rounded-full flex items-center justify-center mx-auto">
                                <UserCheck className="w-8 h-8" />
                            </div>
                            <div className="text-center">
                                <h3 className="text-xl font-bold text-emerald-950">Volunteer Responding</h3>
                                <p className="text-xs text-slate-600 mt-1">
                                    Priya Sharma has officially accepted and confirmed en-route ETA 7 min.
                                </p>
                            </div>

                            <Button 
                                size="lg" 
                                variant="success" 
                                className="w-full font-bold"
                                onClick={() => resolveRequest(request.id, 'Assistance provided by Volunteer Priya Sharma.')}
                            >
                                Resolve Incident ✓
                            </Button>
                        </Card>
                    )}

                    {isResolved && (
                        <Card className="p-8 text-center border-2 border-emerald-400 bg-emerald-50 space-y-3">
                            <CheckCircle2 className="w-16 h-16 text-emerald-600 mx-auto" />
                            <h3 className="text-2xl font-black text-emerald-950">Incident Resolved</h3>
                            <p className="text-xs text-emerald-800 font-medium">
                                This request has moved out of active queues and is archived in Request History.
                            </p>
                            <Button 
                                onClick={() => navigate('/history')}
                                className="bg-slate-900 hover:bg-slate-800 text-white font-bold"
                            >
                                View in Request History →
                            </Button>
                        </Card>
                    )}

                </div>

            </div>
        </div>
    );
}
