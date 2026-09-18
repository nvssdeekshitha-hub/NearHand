import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
    ShieldAlert, 
    Users, 
    Activity, 
    CheckCircle2, 
    Clock, 
    MapPin, 
    Phone, 
    PlusCircle
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/common/Modal';
import { useCare } from '../../context/CareContext';
import { mockAdditionalCaretakers } from '../../mock-data/users';

export function CaretakerDashboard() {
    const navigate = useNavigate();
    const { 
        seniors, 
        activeRequests, 
        historyRequests, 
        caretakerAccept, 
        caretakerTimeout, 
        resolveRequest,
        caretakerStatus,
        setCaretakerStatus,
        requestAdditionalSupport
    } = useCare();

    const [supportModalSenior, setSupportModalSenior] = useState(null);
    const [callModalContact, setCallModalContact] = useState(null);
    const [supportDispatchedMsg, setSupportDispatchedMsg] = useState(null);

    const criticalCount = activeRequests.filter(r => r.urgency === 'CRITICAL').length;
    const resolvedCount = historyRequests.length;

    const handleAccept = async (reqId) => {
        await caretakerAccept(reqId);
    };

    const handleTimeout = async (reqId) => {
        await caretakerTimeout(reqId);
    };

    const handleDispatchSupport = async (caretaker) => {
        await requestAdditionalSupport(supportModalSenior?.id || 101, {
            caretakerName: `${caretaker.name} (${caretaker.distance_km} km)`
        });
        setSupportDispatchedMsg(`Support request dispatched to ${caretaker.name}! They will arrive shortly.`);
        setTimeout(() => {
            setSupportDispatchedMsg(null);
            setSupportModalSenior(null);
        }, 3000);
    };

    return (
        <div className="max-w-6xl mx-auto space-y-8 pb-20 animate-fade-in">
            
            {/* Header with Status Toggle */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-200">
                <div>
                    <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                        Good morning, Ravi.
                    </h1>
                    <p className="text-slate-500 font-medium text-sm mt-1">
                        NEARHAND Care Management & Incident Dispatch Hub
                    </p>
                </div>

                <div className="flex items-center space-x-3">
                    <span className="text-xs font-bold uppercase text-slate-400">Status:</span>
                    <button
                        onClick={() => setCaretakerStatus(caretakerStatus === 'Available' ? 'On Scene' : 'Available')}
                        className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-bold border transition-colors ${
                            caretakerStatus === 'Available' 
                                ? 'bg-emerald-50 text-emerald-800 border-emerald-200 hover:bg-emerald-100'
                                : 'bg-amber-50 text-amber-800 border-amber-200 hover:bg-amber-100'
                        }`}
                    >
                        <span className={`w-2.5 h-2.5 rounded-full ${caretakerStatus === 'Available' ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}`} />
                        <span>🟢 {caretakerStatus}</span>
                    </button>
                </div>
            </div>

            {/* KPI Stats Bar */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
                <Card className="p-5 border-l-4 border-l-sky-500">
                    <p className="text-slate-500 font-bold text-xs uppercase tracking-wider">Assigned Seniors</p>
                    <p className="text-3xl font-black text-slate-900 mt-2">{seniors.length}</p>
                    <p className="text-[11px] text-slate-400 mt-1">All under primary coverage</p>
                </Card>

                <Card className={`p-5 border-l-4 ${activeRequests.length > 0 ? 'border-l-rose-500 bg-rose-50/20' : 'border-l-slate-300'}`}>
                    <p className="text-rose-700 font-bold text-xs uppercase tracking-wider">Active Requests</p>
                    <p className="text-3xl font-black text-rose-600 mt-2">{activeRequests.length}</p>
                    <p className="text-[11px] text-rose-600/80 mt-1">Requires active attention</p>
                </Card>

                <Card className="p-5 border-l-4 border-l-amber-500">
                    <p className="text-amber-700 font-bold text-xs uppercase tracking-wider">Critical Alerts</p>
                    <p className="text-3xl font-black text-amber-600 mt-2">{criticalCount}</p>
                    <p className="text-[11px] text-amber-700/80 mt-1">Urgent response priority</p>
                </Card>

                <Card className="p-5 border-l-4 border-l-emerald-500">
                    <p className="text-emerald-700 font-bold text-xs uppercase tracking-wider">Resolved History</p>
                    <p className="text-3xl font-black text-emerald-600 mt-2">{resolvedCount}</p>
                    <button 
                        onClick={() => navigate('/history')}
                        className="text-[11px] text-sky-600 font-bold hover:underline mt-1 block"
                    >
                        View Full History →
                    </button>
                </Card>
            </div>

            {/* Main Content Grid */}
            <div className="grid lg:grid-cols-3 gap-8">
                
                {/* Active Requests (Left 2 cols) */}
                <div className="lg:col-span-2 space-y-5">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                            <ShieldAlert className="w-5 h-5 text-rose-600" />
                            <h2 className="text-xl font-bold text-slate-900">Active Requests Queue</h2>
                            <span className="text-xs bg-rose-100 text-rose-700 font-bold px-2 py-0.5 rounded-full">
                                {activeRequests.length}
                            </span>
                        </div>
                        <button
                            onClick={() => navigate('/caretaker/requests')}
                            className="text-xs font-bold text-sky-600 hover:text-sky-800"
                        >
                            Manage Requests
                        </button>
                    </div>

                    {activeRequests.length === 0 ? (
                        <Card className="p-12 text-center border-dashed border-2 border-slate-200">
                            <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto mb-3" />
                            <h3 className="text-lg font-bold text-slate-800">All requests clear</h3>
                            <p className="text-sm text-slate-500 mt-1">No active requests currently pending in your queue.</p>
                        </Card>
                    ) : (
                        <div className="space-y-4">
                            {activeRequests.map(req => {
                                const isCritical = req.urgency === 'CRITICAL';
                                const isWaiting = req.status === 'WAITING_FOR_RESPONSE' || req.status === 'CARETAKER_NOTIFIED';
                                const isEscalated = req.status === 'ESCALATED';
                                const isAccepted = req.status === 'ACCEPTED' || req.status === 'IN_PROGRESS';

                                const minutes = Math.floor((req.seconds_remaining || 0) / 60);
                                const seconds = (req.seconds_remaining || 0) % 60;
                                const timerStr = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

                                return (
                                    <Card 
                                        key={req.id} 
                                        className={`p-6 border-2 transition-all relative overflow-hidden ${
                                            isCritical ? 'border-rose-200 shadow-md' : 'border-slate-200'
                                        }`}
                                    >
                                        <div className={`absolute left-0 top-0 bottom-0 w-2 ${
                                            isCritical ? 'bg-rose-600' : 'bg-sky-500'
                                        }`} />

                                        <div className="pl-3">
                                            {/* Header */}
                                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                                                <div className="flex items-center space-x-3">
                                                    <h3 className="text-2xl font-black text-slate-900">
                                                        {req.senior_name}, {req.senior_age}
                                                    </h3>
                                                    <Badge variant={isCritical ? 'critical' : 'warning'}>
                                                        {req.urgency}
                                                    </Badge>
                                                    <span className="text-xs bg-slate-100 text-slate-600 font-semibold px-2 py-0.5 rounded-md">
                                                        Risk: {req.risk_score}/100
                                                    </span>
                                                </div>

                                                <div className="flex items-center space-x-2">
                                                    {isWaiting && (
                                                        <div className="flex items-center text-xs font-mono font-bold bg-rose-50 border border-rose-200 text-rose-700 px-3 py-1 rounded-full">
                                                            <Clock className="w-3.5 h-3.5 mr-1 text-rose-600" />
                                                            <span>{timerStr} remaining</span>
                                                        </div>
                                                    )}
                                                    {isEscalated && (
                                                        <Badge variant="warning">
                                                            ⚡ Caretaker Timeout • Escalated
                                                        </Badge>
                                                    )}
                                                    {isAccepted && (
                                                        <Badge variant="success">
                                                            ✓ In Progress ({req.assigned_volunteer_name ? `Volunteer ${req.assigned_volunteer_name}` : 'You accepted'})
                                                        </Badge>
                                                    )}
                                                </div>
                                            </div>

                                            {/* Situation */}
                                            <p className="text-base font-bold text-slate-800 mb-1">
                                                {req.ai_summary}
                                            </p>
                                            {req.original_transcript && (
                                                <p className="text-xs text-slate-500 italic mb-4">
                                                    "{req.original_transcript}"
                                                </p>
                                            )}

                                            <div className="flex items-center text-xs text-slate-500 mb-5 space-x-4 font-medium">
                                                <span className="flex items-center">
                                                    <MapPin className="w-3.5 h-3.5 mr-1 text-sky-600" /> {req.location}
                                                </span>
                                                <span className="flex items-center">
                                                    <Activity className="w-3.5 h-3.5 mr-1 text-emerald-600" /> Status: {req.status}
                                                </span>
                                            </div>

                                            {/* Action Buttons (Part 5 & Part 15) */}
                                            <div className="flex flex-wrap items-center gap-2.5 pt-3 border-t border-slate-100">
                                                {isWaiting && (
                                                    <Button 
                                                        variant="emergency" 
                                                        size="sm"
                                                        onClick={() => handleAccept(req.id)}
                                                        className="font-bold px-5"
                                                    >
                                                        Accept
                                                    </Button>
                                                )}

                                                <Button 
                                                    variant="secondary" 
                                                    size="sm"
                                                    onClick={() => navigate(`/caretaker/senior/${req.senior_id}`)}
                                                >
                                                    View Profile
                                                </Button>

                                                <Button 
                                                    variant="secondary" 
                                                    size="sm"
                                                    onClick={() => setCallModalContact({ name: req.senior_name, phone: '+91 98765 12345' })}
                                                >
                                                    <Phone className="w-3.5 h-3.5 mr-1.5 text-sky-600" /> Call
                                                </Button>

                                                <Button 
                                                    variant="secondary" 
                                                    size="sm"
                                                    onClick={() => setSupportModalSenior({ id: req.senior_id, name: req.senior_name })}
                                                    className="text-sky-700 border-sky-200 hover:bg-sky-50"
                                                >
                                                    Request Additional Support
                                                </Button>

                                                <Button 
                                                    variant="success" 
                                                    size="sm"
                                                    onClick={() => resolveRequest(req.id, 'Assisted by Caretaker Ravi Kumar.')}
                                                >
                                                    Resolve
                                                </Button>

                                                {isWaiting && (
                                                    <button
                                                        onClick={() => handleTimeout(req.id)}
                                                        className="text-[11px] text-slate-400 hover:text-amber-600 underline ml-auto"
                                                        title="Simulate timer reaching zero"
                                                    >
                                                        Simulate Timeout
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

                {/* Assigned Seniors (Right col) */}
                <div className="space-y-5">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                            <Users className="w-5 h-5 text-sky-600" />
                            <h2 className="text-xl font-bold text-slate-900">My Seniors</h2>
                        </div>
                        <button
                            onClick={() => navigate('/caretaker/seniors')}
                            className="text-xs font-bold text-sky-600 hover:text-sky-800"
                        >
                            View All ({seniors.length})
                        </button>
                    </div>

                    <Card className="divide-y divide-slate-100 overflow-hidden">
                        {seniors.map(senior => {
                            const hasActive = activeRequests.some(r => r.senior_id === senior.id);
                            const activeAlert = activeRequests.find(r => r.senior_id === senior.id);

                            return (
                                <div
                                    key={senior.id}
                                    onClick={() => navigate(`/caretaker/senior/${senior.id}`)}
                                    className="p-4 hover:bg-slate-50 transition-colors flex items-center justify-between cursor-pointer"
                                >
                                    <div>
                                        <p className="font-bold text-slate-900 text-base">{senior.name}, {senior.age}</p>
                                        <p className="text-xs text-slate-500 mt-0.5 flex items-center">
                                            <MapPin className="w-3 h-3 mr-1 text-slate-400" /> {senior.location}
                                        </p>
                                    </div>
                                    <div className="text-right">
                                        <Badge variant={hasActive ? (activeAlert?.urgency === 'CRITICAL' ? 'critical' : 'warning') : 'success'}>
                                            {hasActive ? `${activeAlert?.urgency || 'Active'}` : 'Stable'}
                                        </Badge>
                                    </div>
                                </div>
                            );
                        })}
                    </Card>

                    {/* Quick Support Link Card */}
                    <Card className="p-5 border border-sky-200 bg-sky-50/40">
                        <h4 className="font-bold text-slate-900 text-sm mb-1 flex items-center">
                            <PlusCircle className="w-4 h-4 mr-1.5 text-sky-600" /> Caregiver Co-Dispatch
                        </h4>
                        <p className="text-xs text-slate-600 leading-relaxed mb-3">
                            Need dual-caretaker assistance on site? You can request nearby co-caretakers to assist without unassigning yourself.
                        </p>
                        <Button 
                            variant="secondary" 
                            size="sm" 
                            className="w-full text-xs font-bold text-sky-700"
                            onClick={() => setSupportModalSenior(seniors[0])}
                        >
                            Dispatch Additional Caretaker
                        </Button>
                    </Card>
                </div>

            </div>

            {/* Request Additional Support Modal (Part 17) */}
            <Modal
                isOpen={Boolean(supportModalSenior)}
                onClose={() => setSupportModalSenior(null)}
                title="Request Additional Support"
                maxWidth="max-w-md"
            >
                <div className="space-y-4">
                    <p className="text-sm text-slate-600 leading-relaxed">
                        Currently assisting <span className="font-bold text-slate-900">{supportModalSenior?.name}</span>. Select a nearby available co-caretaker to assist on scene.
                    </p>

                    {supportDispatchedMsg && (
                        <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-800 text-xs font-bold flex items-center animate-fade-in">
                            <CheckCircle2 className="w-4 h-4 mr-2 text-emerald-600" />
                            {supportDispatchedMsg}
                        </div>
                    )}

                    <div className="space-y-2.5">
                        {mockAdditionalCaretakers.map(caregiver => (
                            <div 
                                key={caregiver.id}
                                className="p-4 rounded-2xl border border-slate-200 bg-white hover:border-sky-300 transition-all flex items-center justify-between"
                            >
                                <div>
                                    <h4 className="font-bold text-slate-900 text-sm">{caregiver.name}</h4>
                                    <p className="text-xs text-slate-500 mt-0.5">
                                        📍 {caregiver.distance_km} km away • {caregiver.skills.join(', ')}
                                    </p>
                                    <span className="inline-block text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full mt-1.5">
                                        🟢 {caregiver.status}
                                    </span>
                                </div>
                                <Button 
                                    size="sm"
                                    onClick={() => handleDispatchSupport(caregiver)}
                                    className="bg-sky-600 text-white font-bold"
                                >
                                    Request
                                </Button>
                            </div>
                        ))}
                    </div>

                    <div className="pt-2 text-center">
                        <button
                            onClick={() => setSupportModalSenior(null)}
                            className="text-xs text-slate-400 hover:text-slate-600"
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            </Modal>

            {/* Direct Call Modal */}
            <Modal
                isOpen={Boolean(callModalContact)}
                onClose={() => setCallModalContact(null)}
                title="Direct Phone Call"
                maxWidth="max-w-sm"
            >
                <div className="text-center space-y-4">
                    <div className="w-16 h-16 bg-sky-50 text-sky-600 rounded-full flex items-center justify-center mx-auto border-4 border-sky-100">
                        <Phone className="w-8 h-8" />
                    </div>
                    <div>
                        <h4 className="font-bold text-lg text-slate-900">{callModalContact?.name}</h4>
                        <p className="text-sm text-slate-500 font-mono mt-1">{callModalContact?.phone}</p>
                    </div>
                    <Button 
                        size="lg" 
                        className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-2xl"
                        onClick={() => {
                            alert(`Connecting voice call to ${callModalContact?.name} (${callModalContact?.phone})...`);
                            setCallModalContact(null);
                        }}
                    >
                        Dial Number
                    </Button>
                </div>
            </Modal>

        </div>
    );
}
