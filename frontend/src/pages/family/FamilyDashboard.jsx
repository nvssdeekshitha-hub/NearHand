import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
    Pill, 
    Activity, 
    Clock, 
    ShieldAlert, 
    Heart, 
    CalendarCheck, 
    Phone, 
    MapPin, 
    CheckCircle2, 
    AlertTriangle,
    Navigation,
    ShieldCheck
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/common/Modal';
import { useCare } from '../../context/CareContext';

export function FamilyDashboard() {
    const navigate = useNavigate();
    const { 
        seniors, 
        activeRequests, 
        locationSafety, 
        confirmLocationTrip 
    } = useCare();

    const [mapModalOpen, setMapModalOpen] = useState(false);
    const [callModal, setCallModal] = useState(null);

    const senior = seniors[0]; // Lakshmi
    const seniorActiveRequest = activeRequests.find(r => r.senior_id === 101);

    return (
        <div className="max-w-5xl mx-auto space-y-6 pb-20 animate-fade-in">
            
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
                <div>
                    <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
                        Lakshmi's Care Overview
                    </h1>
                    <p className="text-slate-500 font-medium text-sm mt-0.5">
                        Family Care Portal • Connected to Primary Caretaker & Volunteer Network
                    </p>
                </div>
                <Badge variant={seniorActiveRequest ? 'critical' : 'primary'} className="px-3 py-1 text-xs">
                    {seniorActiveRequest ? '🚨 Active Incident Underway' : '🟢 Safe / No Active Alert'}
                </Badge>
            </div>

            {/* Location Safety Component (Part 21) */}
            <Card className="p-6 border-2 border-amber-200 bg-amber-50/30">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div className="space-y-2">
                        <div className="flex items-center space-x-2">
                            <AlertTriangle className="w-5 h-5 text-amber-600" />
                            <h3 className="font-bold text-slate-900 text-lg">Location Safety Monitor</h3>
                            <Badge variant={locationSafety.expected === true ? 'success' : 'warning'}>
                                {locationSafety.status}
                            </Badge>
                        </div>
                        
                        <div className="grid sm:grid-cols-2 gap-3 text-xs pt-1">
                            <div className="bg-white p-3 rounded-xl border border-amber-100">
                                <span className="font-bold text-slate-400 uppercase text-[10px] block">Designated Home</span>
                                <span className="font-bold text-slate-800 text-sm">{locationSafety.home}</span>
                            </div>
                            <div className="bg-white p-3 rounded-xl border border-amber-100">
                                <span className="font-bold text-slate-400 uppercase text-[10px] block">Current Location</span>
                                <span className="font-bold text-slate-800 text-sm flex items-center">
                                    <MapPin className="w-3.5 h-3.5 mr-1 text-amber-600" /> {locationSafety.currentLocation}
                                </span>
                            </div>
                        </div>

                        <p className="text-xs text-slate-600 mt-2">
                            Caretaker Ravi Kumar was informed. Moving away from home does not automatically mean danger.
                        </p>
                    </div>

                    {/* Verification Prompt */}
                    <div className="flex flex-col gap-2.5 bg-white p-4 rounded-2xl border border-amber-200 shrink-0 w-full md:w-64 text-center">
                        <p className="text-xs font-bold text-slate-900">Expected trip?</p>
                        <div className="grid grid-cols-2 gap-2">
                            <Button 
                                size="sm" 
                                variant={locationSafety.expected === true ? 'success' : 'secondary'}
                                onClick={() => confirmLocationTrip(true)}
                                className="text-xs font-bold"
                            >
                                ✓ Yes, Expected
                            </Button>
                            <Button 
                                size="sm" 
                                variant={locationSafety.expected === false ? 'emergency' : 'secondary'}
                                onClick={() => confirmLocationTrip(false)}
                                className="text-xs font-bold text-rose-700"
                            >
                                ✕ No, Unexpected
                            </Button>
                        </div>
                        <button
                            onClick={() => setMapModalOpen(true)}
                            className="text-xs text-sky-600 hover:text-sky-800 font-semibold underline mt-1"
                        >
                            View on Map
                        </button>
                    </div>
                </div>
            </Card>

            <div className="grid lg:grid-cols-3 gap-6">
                
                {/* Left 2 Cols: Health & Activity */}
                <div className="lg:col-span-2 space-y-6">
                    
                    {/* Today's Health */}
                    <Card className="p-6 border-slate-200">
                        <h2 className="text-lg font-bold text-slate-900 mb-4 flex items-center">
                            <Activity className="w-5 h-5 mr-2 text-sky-600" /> Today's Health & Routine
                        </h2>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100 text-center">
                                <Pill className="w-6 h-6 text-emerald-600 mx-auto mb-1.5" />
                                <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Medications</p>
                                <p className="text-2xl font-black text-slate-900 mt-0.5">4 / 4</p>
                                <p className="text-xs text-emerald-700 font-semibold mt-1">All doses on schedule</p>
                            </div>
                            <div className="bg-emerald-50/50 p-4 rounded-2xl border border-emerald-100 text-center">
                                <CalendarCheck className="w-6 h-6 text-emerald-600 mx-auto mb-1.5" />
                                <p className="text-[11px] font-bold text-emerald-800 uppercase tracking-wider">Daily Check-in</p>
                                <p className="text-2xl font-black text-emerald-950 mt-0.5">Completed</p>
                                <p className="text-xs text-emerald-700 font-semibold mt-1">Verified at 08:00 AM</p>
                            </div>
                        </div>
                    </Card>

                    {/* Real-time Activity Timeline */}
                    <Card className="p-6 border-slate-200">
                        <h2 className="text-lg font-bold text-slate-900 mb-5 flex items-center">
                            <Clock className="w-5 h-5 mr-2 text-sky-600" /> Recent Activity & Event Timeline
                        </h2>
                        
                        <div className="relative border-l-2 border-slate-200 ml-3 space-y-6 text-xs">
                            <div className="relative pl-6">
                                <span className="absolute -left-[9px] top-0.5 w-4 h-4 rounded-full bg-slate-300 ring-4 ring-white" />
                                <p className="font-bold text-sm text-slate-900">Medication taken (Amlodipine 5mg)</p>
                                <p className="text-slate-500">08:00 AM • Logged by Lakshmi</p>
                            </div>

                            <div className="relative pl-6">
                                <span className="absolute -left-[9px] top-0.5 w-4 h-4 rounded-full bg-slate-300 ring-4 ring-white" />
                                <p className="font-bold text-sm text-slate-900">Caretaker morning check-in</p>
                                <p className="text-slate-500">10:30 AM • Confirmed by Ravi Kumar</p>
                            </div>

                            {seniorActiveRequest && (
                                <>
                                    <div className="relative pl-6">
                                        <span className="absolute -left-[17px] top-0 bg-rose-600 text-white rounded-full p-1 border-4 border-white animate-pulse">
                                            <ShieldAlert className="w-3 h-3" />
                                        </span>
                                        <p className="font-bold text-sm text-rose-700">
                                            Help request ({seniorActiveRequest.request_type}) created
                                        </p>
                                        <p className="text-slate-500">13:10 PM • Urgency: {seniorActiveRequest.urgency}</p>
                                    </div>

                                    {seniorActiveRequest.assigned_volunteer_name && (
                                        <div className="relative pl-6">
                                            <span className="absolute -left-[9px] top-0.5 w-4 h-4 rounded-full bg-emerald-500 ring-4 ring-white" />
                                            <p className="font-bold text-sm text-emerald-800">
                                                Volunteer {seniorActiveRequest.assigned_volunteer_name} accepted assistance
                                            </p>
                                            <p className="text-slate-500">13:12 PM • ETA ~7 min to location</p>
                                        </div>
                                    )}
                                </>
                            )}
                        </div>
                    </Card>

                </div>

                {/* Right Col: Alerts & Care Team */}
                <div className="space-y-6">
                    
                    {/* Alerts Panel */}
                    <Card className={`p-5 ${seniorActiveRequest ? 'border-2 border-rose-200 bg-rose-50/30' : 'border-slate-200'}`}>
                        <h3 className="font-bold text-slate-900 text-sm mb-3 flex items-center">
                            <ShieldAlert className="w-4 h-4 mr-2 text-rose-600" /> Active Alerts
                        </h3>

                        {seniorActiveRequest ? (
                            <div className="space-y-2">
                                <div className="p-3 bg-white rounded-xl border border-rose-200 text-xs">
                                    <p className="font-bold text-rose-700">{seniorActiveRequest.ai_summary}</p>
                                    <p className="text-slate-500 mt-1">Status: {seniorActiveRequest.status}</p>
                                    <button 
                                        onClick={() => navigate(`/request/${seniorActiveRequest.id}`)}
                                        className="text-sky-600 font-bold underline mt-2 block"
                                    >
                                        Track Live Response →
                                    </button>
                                </div>
                            </div>
                        ) : (
                            <p className="text-xs text-slate-500">No active emergency alerts at this time.</p>
                        )}
                    </Card>

                    {/* Care Team Contacts */}
                    <Card className="p-5 border-slate-200 space-y-4">
                        <h3 className="font-bold text-slate-900 text-sm flex items-center">
                            <Heart className="w-4 h-4 mr-2 text-rose-500" /> Connected Care Team
                        </h3>

                        <div className="space-y-3 text-xs">
                            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 flex items-center justify-between">
                                <div>
                                    <p className="font-bold text-slate-900">Ravi Kumar</p>
                                    <p className="text-slate-500">Primary Caretaker</p>
                                    <span className="text-[10px] text-emerald-700 font-bold">🟢 Available</span>
                                </div>
                                <Button 
                                    size="sm" 
                                    variant="secondary"
                                    onClick={() => setCallModal({ name: 'Ravi Kumar (Caretaker)', phone: '+91 98765 43210' })}
                                >
                                    <Phone className="w-3.5 h-3.5" />
                                </Button>
                            </div>

                            <div className="p-3 bg-sky-50 rounded-xl border border-sky-100 flex items-center justify-between">
                                <div>
                                    <p className="font-bold text-slate-900">Priya Sharma</p>
                                    <p className="text-slate-500">Community Volunteer Network</p>
                                    <span className="text-[10px] text-sky-700 font-bold">🟢 On Standby</span>
                                </div>
                                <Button 
                                    size="sm" 
                                    variant="secondary"
                                    onClick={() => setCallModal({ name: 'Priya Sharma (Volunteer)', phone: '+91 94401 23456' })}
                                >
                                    <Phone className="w-3.5 h-3.5" />
                                </Button>
                            </div>
                        </div>
                    </Card>

                </div>

            </div>

            {/* Map Modal */}
            <Modal
                isOpen={mapModalOpen}
                onClose={() => setMapModalOpen(false)}
                title="Location Map Safety View"
                maxWidth="max-w-md"
            >
                <div className="text-center space-y-4">
                    <div className="w-full h-48 bg-slate-100 rounded-2xl border border-slate-200 flex flex-col items-center justify-center p-4">
                        <Navigation className="w-10 h-10 text-sky-600 mb-2 animate-pulse" />
                        <p className="font-bold text-slate-800 text-sm">GPS Tracking Active</p>
                        <p className="text-xs text-slate-500 mt-1">2.8 km away at MG Road Junction, Vijayawada</p>
                    </div>
                    <Button className="w-full font-bold" onClick={() => setMapModalOpen(false)}>
                        Dismiss
                    </Button>
                </div>
            </Modal>

            {/* Call Modal */}
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
