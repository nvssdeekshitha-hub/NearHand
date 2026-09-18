import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
    ArrowLeft, 
    UserCircle2, 
    MapPin, 
    HeartPulse, 
    Pill, 
    CheckCircle2, 
    Clock, 
    ShieldAlert, 
    Phone, 
    AlertTriangle, 
    Users,
    PlusCircle
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/common/Modal';
import { useCare } from '../../context/CareContext';
import { mockAdditionalCaretakers } from '../../mock-data/users';

export function CaretakerSeniorDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const { seniors, requests, requestAdditionalSupport } = useCare();

    const [isSupportModalOpen, setIsSupportModalOpen] = useState(false);
    const [supportDispatched, setSupportDispatched] = useState(null);
    const [callModal, setCallModal] = useState(null);

    const senior = seniors.find(s => s.id === Number(id)) || seniors[0];
    const seniorRequests = requests.filter(r => r.senior_id === senior.id);

    const handleDispatchSupport = async (caregiver) => {
        await requestAdditionalSupport(senior.id, {
            caretakerName: `${caregiver.name} (${caregiver.distance_km} km)`
        });
        setSupportDispatched(`Support successfully dispatched to ${caregiver.name}.`);
        setTimeout(() => {
            setSupportDispatched(null);
            setIsSupportModalOpen(false);
        }, 3000);
    };

    return (
        <div className="max-w-5xl mx-auto space-y-6 pb-20 animate-fade-in">
            {/* Top Navigation */}
            <div>
                <button
                    onClick={() => navigate('/caretaker/seniors')}
                    className="inline-flex items-center text-xs font-bold text-slate-500 hover:text-sky-600 transition-colors"
                >
                    <ArrowLeft className="w-3.5 h-3.5 mr-1" /> Back to Seniors List
                </button>
            </div>

            <div className="grid lg:grid-cols-3 gap-6">
                
                {/* Left Profile Card */}
                <div className="space-y-6">
                    <Card className="p-6 text-center border-slate-200">
                        <div className="w-24 h-24 rounded-full bg-sky-50 border-4 border-sky-100 flex items-center justify-center mx-auto mb-4 text-sky-600">
                            <UserCircle2 className="w-14 h-14" />
                        </div>

                        <h1 className="text-2xl font-black text-slate-900">{senior.name}</h1>
                        <p className="text-xs text-slate-500 font-medium mt-0.5">
                            {senior.age} years old • {senior.gender}
                        </p>

                        <div className="my-4">
                            <Badge variant="success" className="px-3 py-1 text-xs">
                                🟢 {senior.status || 'Checked in'}
                            </Badge>
                        </div>

                        <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100 text-left space-y-2.5 text-xs text-slate-600 my-5">
                            <div className="flex items-center">
                                <MapPin className="w-3.5 h-3.5 mr-2 text-sky-600 shrink-0" />
                                <span>{senior.address || senior.location}</span>
                            </div>
                            <div className="flex items-center">
                                <Users className="w-3.5 h-3.5 mr-2 text-sky-600 shrink-0" />
                                <span>Family: Anjali (Daughter)</span>
                            </div>
                            <div className="flex items-center">
                                <HeartPulse className="w-3.5 h-3.5 mr-2 text-rose-600 shrink-0" />
                                <span>Blood Group: <strong className="text-slate-900">{senior.blood_group || 'O+'}</strong></span>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <Button 
                                className="w-full font-bold text-sm"
                                onClick={() => setCallModal({ name: 'Anjali (Daughter)', phone: '+91 98480 11223' })}
                            >
                                <Phone className="w-3.5 h-3.5 mr-1.5" /> Contact Family
                            </Button>
                            <Button 
                                variant="secondary" 
                                className="w-full text-xs font-semibold text-slate-700"
                                onClick={() => setCallModal({ name: senior.name, phone: '+91 98765 12345' })}
                            >
                                Call Senior Directly
                            </Button>
                        </div>
                    </Card>

                    {/* Additional Support Callout (Part 17) */}
                    <Card className="p-5 border border-sky-200 bg-sky-50/50">
                        <div className="flex items-center space-x-2 text-sky-900 font-bold text-sm mb-2">
                            <PlusCircle className="w-4 h-4 text-sky-600" />
                            <span>Need Additional Support?</span>
                        </div>
                        <p className="text-xs text-slate-600 leading-relaxed mb-4">
                            If you require a second pair of hands on site for transfer, mobility, or observation, dispatch a nearby co-caretaker.
                        </p>
                        <Button 
                            variant="secondary"
                            size="sm"
                            className="w-full font-bold border-sky-300 text-sky-700 hover:bg-sky-100 text-xs"
                            onClick={() => setIsSupportModalOpen(true)}
                        >
                            Request Additional Support
                        </Button>
                    </Card>
                </div>

                {/* Right Details (Health Summary, Medications, History) */}
                <div className="lg:col-span-2 space-y-6">
                    
                    {/* Health Summary */}
                    <Card className="p-6 border-slate-200">
                        <h2 className="text-lg font-bold text-slate-900 mb-4 flex items-center border-b border-slate-100 pb-3">
                            <HeartPulse className="w-5 h-5 text-rose-500 mr-2" /> Health Summary
                        </h2>

                        <div className="grid sm:grid-cols-2 gap-6">
                            <div>
                                <p className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                                    Medical Conditions
                                </p>
                                <div className="flex flex-wrap gap-2">
                                    {senior.conditions?.map(cond => (
                                        <span key={cond} className="px-3 py-1 bg-amber-50 text-amber-800 text-xs font-bold rounded-lg border border-amber-200">
                                            {cond}
                                        </span>
                                    ))}
                                </div>
                            </div>

                            <div>
                                <p className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                                    Allergies
                                </p>
                                <div className="flex flex-wrap gap-2">
                                    {senior.allergies?.map(all => (
                                        <span key={all} className="px-3 py-1 bg-rose-50 text-rose-800 text-xs font-bold rounded-lg border border-rose-200">
                                            {all}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {senior.notes && (
                            <div className="mt-5 pt-4 border-t border-slate-100">
                                <p className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">
                                    Clinical / Care Notes
                                </p>
                                <p className="text-xs text-slate-700 font-medium">
                                    {senior.notes}
                                </p>
                            </div>
                        )}
                    </Card>

                    {/* Medications Checklist */}
                    <Card className="p-6 border-slate-200">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
                            <h2 className="text-lg font-bold text-slate-900 flex items-center">
                                <Pill className="w-5 h-5 text-emerald-600 mr-2" /> Today's Medications
                            </h2>
                            <Badge variant="success" className="text-xs">
                                {senior.medications?.filter(m => m.taken).length} / {senior.medications?.length} Taken
                            </Badge>
                        </div>

                        <div className="space-y-2.5">
                            {senior.medications?.map(med => (
                                <div 
                                    key={med.id}
                                    className={`p-3.5 rounded-2xl border flex items-center justify-between text-xs ${
                                        med.taken 
                                            ? 'bg-emerald-50/50 border-emerald-100 text-slate-800' 
                                            : 'bg-white border-slate-200 text-slate-700'
                                    }`}
                                >
                                    <div className="flex items-center space-x-3">
                                        {med.taken ? (
                                            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
                                        ) : (
                                            <div className="w-5 h-5 rounded-full border-2 border-slate-300 shrink-0" />
                                        )}
                                        <div>
                                            <p className="font-bold text-sm text-slate-900">{med.name}</p>
                                            <p className="text-slate-500 mt-0.5">{med.time}</p>
                                        </div>
                                    </div>
                                    <span className={`font-bold px-2.5 py-0.5 rounded-full text-[11px] ${
                                        med.taken ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-600'
                                    }`}>
                                        {med.taken ? '✓ Taken' : '○ Pending'}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </Card>

                    {/* Recent Requests Timeline */}
                    <Card className="p-6 border-slate-200">
                        <h2 className="text-lg font-bold text-slate-900 mb-5 flex items-center border-b border-slate-100 pb-3">
                            <Clock className="w-5 h-5 text-sky-600 mr-2" /> Requests & Care Activity
                        </h2>

                        {seniorRequests.length === 0 ? (
                            <p className="text-xs text-slate-400 italic">No recent requests recorded for this senior.</p>
                        ) : (
                            <div className="relative border-l-2 border-slate-200 ml-3 space-y-6">
                                {seniorRequests.map((req, idx) => {
                                    const isCritical = req.urgency === 'CRITICAL';
                                    return (
                                        <div key={req.id} className="relative pl-6 text-xs">
                                            <span className={`absolute -left-[9px] top-0.5 w-4 h-4 rounded-full ring-4 ring-white ${
                                                req.status === 'RESOLVED' 
                                                    ? 'bg-emerald-500' 
                                                    : isCritical 
                                                    ? 'bg-rose-500 animate-pulse' 
                                                    : 'bg-sky-500'
                                            }`} />
                                            
                                            <div className="flex items-center justify-between">
                                                <p className="font-bold text-sm text-slate-900">{req.ai_summary || req.request_type}</p>
                                                <Badge variant={req.status === 'RESOLVED' ? 'success' : isCritical ? 'critical' : 'warning'}>
                                                    {req.status}
                                                </Badge>
                                            </div>

                                            {req.original_transcript && (
                                                <p className="text-slate-600 italic mt-1">"{req.original_transcript}"</p>
                                            )}

                                            <div className="flex items-center space-x-3 text-slate-400 mt-1.5 text-[11px]">
                                                <span>#{req.id}</span>
                                                <span>•</span>
                                                <span>Priority: {req.risk_score}/100</span>
                                                <span>•</span>
                                                <span>Assigned: {req.assigned_volunteer_name || req.assigned_caretaker_name}</span>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                    </Card>

                </div>
            </div>

            {/* Additional Support Modal */}
            <Modal
                isOpen={isSupportModalOpen}
                onClose={() => setIsSupportModalOpen(false)}
                title={`Request Additional Support for ${senior.name}`}
                maxWidth="max-w-md"
            >
                <div className="space-y-4 text-xs">
                    <p className="text-slate-600 leading-relaxed">
                        Dispatch a nearby professional caregiver to assist you on-scene at <strong className="text-slate-900">{senior.location}</strong>.
                    </p>

                    {supportDispatched && (
                        <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-emerald-800 font-bold flex items-center animate-fade-in">
                            <CheckCircle2 className="w-4 h-4 mr-2 text-emerald-600" />
                            {supportDispatched}
                        </div>
                    )}

                    <div className="space-y-2.5">
                        {mockAdditionalCaretakers.map(caregiver => (
                            <div key={caregiver.id} className="p-3.5 rounded-2xl border border-slate-200 flex items-center justify-between">
                                <div>
                                    <h4 className="font-bold text-slate-900 text-sm">{caregiver.name}</h4>
                                    <p className="text-slate-500 mt-0.5">📍 {caregiver.distance_km} km away • {caregiver.skills.join(', ')}</p>
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
