import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
    Mic, 
    Activity, 
    Pill, 
    Heart, 
    Users, 
    Phone, 
    User as UserIcon, 
    CalendarCheck,
    MessageCircleHeart,
    CheckCircle2,
    ShieldAlert
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { useAuth } from '../../context/AuthContext';
import { useCare } from '../../context/CareContext';
import { EmergencySOSModal } from '../../components/emergency/EmergencySOSModal';
import { EmergencyStatusTracker } from '../../components/emergency/EmergencyStatusTracker';

export function SeniorDashboard() {
    const navigate = useNavigate();
    const { user } = useAuth();
    const { 
        emergencySOS, 
        activateEmergencySOS, 
        cancelEmergencySOS, 
        requestCompanionship 
    } = useCare();

    const [isSOSModalOpen, setIsSOSModalOpen] = useState(false);
    const [companionshipSuccess, setCompanionshipSuccess] = useState(false);
    const [callModal, setCallModal] = useState(null);

    const handleCompanionship = async () => {
        await requestCompanionship(101, 'Lakshmi requested a friendly companion visit.');
        setCompanionshipSuccess(true);
        setTimeout(() => setCompanionshipSuccess(false), 5000);
    };

    return (
        <div className="max-w-3xl mx-auto space-y-8 pb-24 animate-fade-in">
            {/* Header */}
            <div className="text-center md:text-left pt-2 pb-4">
                <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 tracking-tight">
                    Good morning, {user?.name || 'Lakshmi'} 👋
                </h1>
                <p className="text-lg sm:text-xl text-slate-600 mt-2 font-medium">
                    Your care team is here for you.
                </p>
            </div>

            {/* If Emergency SOS is active, show tracker at top */}
            {emergencySOS.active ? (
                <EmergencyStatusTracker onCancel={cancelEmergencySOS} />
            ) : (
                /* Primary Emergency SOS Button */
                <div className="w-full">
                    <button
                        onClick={() => setIsSOSModalOpen(true)}
                        className="w-full py-6 sm:py-7 px-8 bg-rose-600 hover:bg-rose-700 text-white rounded-3xl shadow-xl shadow-rose-600/30 flex items-center justify-center space-x-3 text-2xl sm:text-3xl font-black tracking-wider transition-all transform hover:scale-[1.01] active:scale-[0.99] border-2 border-rose-500 animate-emergency-pulse"
                    >
                        <ShieldAlert className="w-9 h-9 sm:w-10 sm:h-10 shrink-0" />
                        <span>🚨 EMERGENCY SOS</span>
                    </button>
                    <p className="text-center text-xs text-slate-400 mt-2">
                        Press once for immediate emergency assistance and priority notification.
                    </p>
                </div>
            )}

            {/* How Can We Help Section */}
            <Card className="p-6 sm:p-8 border-2 border-sky-200 bg-sky-50/50 rounded-3xl">
                <h2 className="text-2xl font-bold text-slate-900 mb-4">How can we help?</h2>

                <div
                    onClick={() => navigate('/senior/request')}
                    className="bg-white p-5 rounded-2xl border-2 border-sky-200 text-slate-400 text-lg font-medium mb-6 cursor-pointer hover:border-sky-400 transition-colors shadow-xs flex items-center justify-between"
                >
                    <span>Tell us what you need...</span>
                    <Mic className="w-6 h-6 text-sky-600" />
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <Button 
                        size="lg"
                        onClick={() => navigate('/senior/request?mode=speak')} 
                        className="py-4 text-lg bg-sky-600 hover:bg-sky-700 text-white rounded-2xl shadow-sky-600/20 shadow-md font-bold"
                    >
                        <Mic className="w-5 h-5 mr-2" /> Speak
                    </Button>
                    <Button 
                        size="lg"
                        variant="secondary" 
                        onClick={() => navigate('/senior/request?mode=type')} 
                        className="py-4 text-lg rounded-2xl bg-white border-2 border-slate-200 font-bold"
                    >
                        ⌨ Type
                    </Button>
                </div>
            </Card>

            {/* Quick Actions */}
            <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 px-1">
                    Quick Assistance Categories
                </h3>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
                    {[
                        { icon: Activity, label: 'Medical Help', category: 'Medical', color: 'text-amber-600', bg: 'bg-amber-50', border: 'hover:border-amber-300' },
                        { icon: Pill, label: 'Medicine', category: 'Medication', color: 'text-emerald-600', bg: 'bg-emerald-50', border: 'hover:border-emerald-300' },
                        { icon: Users, label: 'Assistance', category: 'Assistance', color: 'text-sky-600', bg: 'bg-sky-50', border: 'hover:border-sky-300' },
                        { icon: Heart, label: 'Feeling Alone', category: 'Companionship', color: 'text-rose-600', bg: 'bg-rose-50', border: 'hover:border-rose-300' }
                    ].map((action) => (
                        <button
                            key={action.label}
                            onClick={() => navigate(`/senior/request?category=${action.category}`)}
                            className={`bg-white p-5 rounded-3xl shadow-xs border border-slate-200 ${action.border} hover:shadow-md transition-all flex flex-col items-center justify-center text-center group cursor-pointer`}
                        >
                            <div className={`w-14 h-14 ${action.bg} rounded-2xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform`}>
                                <action.icon className={`w-7 h-7 ${action.color}`} />
                            </div>
                            <span className="font-bold text-slate-800 text-sm sm:text-base">{action.label}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Companionship Feature (Part 22) */}
            <Card className="p-6 border border-sky-200 bg-gradient-to-r from-sky-50 to-indigo-50/50 rounded-3xl">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div className="flex items-start space-x-3.5">
                        <div className="w-12 h-12 rounded-2xl bg-sky-100 flex items-center justify-center shrink-0">
                            <MessageCircleHeart className="w-6 h-6 text-sky-600" />
                        </div>
                        <div>
                            <h3 className="text-xl font-bold text-slate-900">Feeling alone?</h3>
                            <p className="text-sm text-slate-600 mt-0.5 font-medium">
                                Let your care team know you'd like some company or a friendly call.
                            </p>
                        </div>
                    </div>

                    <Button 
                        onClick={handleCompanionship}
                        className="bg-sky-600 hover:bg-sky-700 text-white font-bold px-6 py-3 rounded-2xl shrink-0 text-sm shadow-md"
                    >
                        💙 Request Company
                    </Button>
                </div>

                {companionshipSuccess && (
                    <div className="mt-4 p-3.5 bg-emerald-50 border border-emerald-200 rounded-2xl text-emerald-800 text-xs font-bold flex items-center animate-fade-in">
                        <CheckCircle2 className="w-4 h-4 mr-2 text-emerald-600" />
                        Companionship request dispatched! Ravi Kumar has been notified for a friendly visit.
                    </div>
                )}
            </Card>

            {/* My Care Team & Today's Status */}
            <div className="grid md:grid-cols-2 gap-6">
                
                {/* Care Team */}
                <Card className="p-6 rounded-3xl border-slate-200">
                    <h2 className="text-lg font-bold text-slate-900 mb-5 flex items-center">
                        <UserIcon className="w-5 h-5 mr-2 text-sky-600" /> My Care Team
                    </h2>
                    <div className="space-y-3.5">
                        <div className="flex items-center justify-between p-4 bg-slate-50 rounded-2xl border border-slate-100">
                            <div>
                                <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Primary Caretaker</p>
                                <p className="text-base font-bold text-slate-900 mt-0.5">Ravi Kumar</p>
                            </div>
                            <div className="flex items-center space-x-2">
                                <Badge variant="success" className="px-2.5 py-1 text-xs">🟢 Available</Badge>
                                <button 
                                    onClick={() => setCallModal('Ravi Kumar (+91 98765 43210)')}
                                    className="p-2 bg-white rounded-xl border border-slate-200 hover:bg-slate-100 text-sky-600 transition-colors"
                                    title="Call Caretaker"
                                >
                                    <Phone className="w-4 h-4" />
                                </button>
                            </div>
                        </div>

                        <div className="flex items-center justify-between p-4 bg-slate-50 rounded-2xl border border-slate-100">
                            <div>
                                <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Family Member</p>
                                <p className="text-base font-bold text-slate-900 mt-0.5">Anjali (Daughter)</p>
                            </div>
                            <div className="flex items-center space-x-2">
                                <Badge variant="primary" className="px-2.5 py-1 text-xs">🟢 Available</Badge>
                                <button 
                                    onClick={() => setCallModal('Anjali (+91 98480 11223)')}
                                    className="p-2 bg-white rounded-xl border border-slate-200 hover:bg-slate-100 text-sky-600 transition-colors"
                                    title="Call Family"
                                >
                                    <Phone className="w-4 h-4" />
                                </button>
                            </div>
                        </div>
                    </div>
                </Card>

                {/* Today's Care */}
                <Card className="p-6 rounded-3xl border-slate-200">
                    <h2 className="text-lg font-bold text-slate-900 mb-5 flex items-center">
                        <Activity className="w-5 h-5 mr-2 text-emerald-600" /> Today's Care
                    </h2>
                    <div className="space-y-3.5">
                        <div className="flex items-center p-4 bg-emerald-50/70 rounded-2xl border border-emerald-100">
                            <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center mr-3.5 shrink-0">
                                <Pill className="w-5 h-5" />
                            </div>
                            <div>
                                <p className="text-[11px] font-bold text-emerald-800 uppercase tracking-wider">Medication</p>
                                <p className="text-lg font-black text-emerald-950 mt-0.5">4 / 4 Taken</p>
                            </div>
                        </div>

                        <div className="flex items-center p-4 bg-sky-50/70 rounded-2xl border border-sky-100">
                            <div className="w-10 h-10 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center mr-3.5 shrink-0">
                                <CalendarCheck className="w-5 h-5" />
                            </div>
                            <div>
                                <p className="text-[11px] font-bold text-sky-800 uppercase tracking-wider">Daily Check-in</p>
                                <p className="text-lg font-black text-sky-950 mt-0.5">Completed (08:00 AM)</p>
                            </div>
                        </div>
                    </div>
                </Card>

            </div>

            {/* Emergency SOS Modal */}
            <EmergencySOSModal
                isOpen={isSOSModalOpen}
                onClose={() => setIsSOSModalOpen(false)}
                onConfirm={activateEmergencySOS}
            />

            {/* Call Confirmation Dialog */}
            {callModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4 animate-fade-in">
                    <Card className="max-w-sm w-full p-6 text-center">
                        <Phone className="w-12 h-12 text-sky-600 mx-auto mb-3" />
                        <h3 className="font-bold text-lg text-slate-900 mb-1">Direct Call</h3>
                        <p className="text-slate-600 text-sm mb-6">{callModal}</p>
                        <Button className="w-full font-bold" onClick={() => setCallModal(null)}>Close</Button>
                    </Card>
                </div>
            )}
        </div>
    );
}
