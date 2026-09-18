import React from 'react';
import { ShieldAlert, MapPin, Clock, CheckCircle2, PhoneCall, AlertTriangle, ShieldCheck } from 'lucide-react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';

export function EmergencyStatusTracker({ onCancel, location = "Plot 42, Moghalrajpuram, Vijayawada" }) {
    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Main Red Alert Banner */}
            <div className="bg-rose-600 text-white p-6 sm:p-8 rounded-3xl shadow-xl shadow-rose-600/20 border border-rose-700 text-center relative overflow-hidden">
                <div className="w-20 h-20 bg-white text-rose-600 rounded-full flex items-center justify-center mx-auto mb-4 border-4 border-rose-200 shadow-inner animate-emergency-pulse">
                    <ShieldAlert className="w-10 h-10" />
                </div>
                <h1 className="text-3xl sm:text-4xl font-black tracking-wider uppercase mb-2">
                    🚨 EMERGENCY ACTIVE
                </h1>
                <p className="text-rose-100 text-base sm:text-lg font-medium max-w-lg mx-auto">
                    Response monitoring is active. Priority dispatch protocols have been initiated.
                </p>
                
                {onCancel && (
                    <button 
                        onClick={onCancel}
                        className="mt-6 px-5 py-2 bg-white/20 hover:bg-white/30 text-white font-semibold text-xs rounded-full border border-white/40 transition-colors"
                    >
                        Deactivate SOS (False Alarm)
                    </button>
                )}
            </div>

            {/* Location and Trigger Info */}
            <Card className="p-6">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="flex items-center space-x-3 p-3 bg-slate-50 rounded-2xl border border-slate-100">
                        <MapPin className="w-6 h-6 text-rose-600 shrink-0" />
                        <div>
                            <p className="text-xs font-bold uppercase text-slate-400">Current Location</p>
                            <p className="font-bold text-slate-900 text-sm mt-0.5">{location}</p>
                        </div>
                    </div>
                    <div className="flex items-center space-x-3 p-3 bg-slate-50 rounded-2xl border border-slate-100">
                        <Clock className="w-6 h-6 text-rose-600 shrink-0" />
                        <div>
                            <p className="text-xs font-bold uppercase text-slate-400">Time Triggered</p>
                            <p className="font-bold text-slate-900 text-sm mt-0.5">{currentTime} (Today)</p>
                        </div>
                    </div>
                </div>
            </Card>

            {/* Live Status Timeline */}
            <Card className="p-6 sm:p-8">
                <h2 className="text-lg font-bold text-slate-900 mb-6 uppercase tracking-wider flex items-center">
                    <ShieldCheck className="w-5 h-5 text-emerald-600 mr-2" /> Live Status Timeline
                </h2>

                <div className="relative border-l-2 border-slate-200 ml-4 space-y-6">
                    <div className="relative pl-6">
                        <span className="absolute -left-[17px] top-0.5 bg-emerald-500 text-white rounded-full p-1 border-4 border-white">
                            <CheckCircle2 className="w-3.5 h-3.5" />
                        </span>
                        <h4 className="font-bold text-slate-900">Caretaker Notified ✓</h4>
                        <p className="text-xs text-slate-500 mt-0.5">High-priority alert dispatched to Ravi Kumar (+91 98765 43210)</p>
                    </div>

                    <div className="relative pl-6">
                        <span className="absolute -left-[17px] top-0.5 bg-emerald-500 text-white rounded-full p-1 border-4 border-white">
                            <CheckCircle2 className="w-3.5 h-3.5" />
                        </span>
                        <h4 className="font-bold text-slate-900">Family Notified ✓</h4>
                        <p className="text-xs text-slate-500 mt-0.5">Automated SMS and in-app alert sent to Anjali (Daughter)</p>
                    </div>

                    <div className="relative pl-6">
                        <span className="absolute -left-[17px] top-0.5 bg-sky-500 text-white rounded-full p-1 border-4 border-white">
                            <CheckCircle2 className="w-3.5 h-3.5" />
                        </span>
                        <h4 className="font-bold text-slate-900">Emergency support pathway initiated ✓</h4>
                        <p className="text-xs text-slate-500 mt-0.5">Volunteer network standby active; nearest responder Priya Sharma (2.4 km)</p>
                    </div>

                    <div className="relative pl-6">
                        <span className="absolute -left-[17px] top-0.5 bg-amber-500 text-white rounded-full p-1 border-4 border-white animate-pulse">
                            <AlertTriangle className="w-3.5 h-3.5" />
                        </span>
                        <h4 className="font-bold text-amber-800">Response Monitoring Active</h4>
                        <p className="text-xs text-amber-700 mt-0.5">Tracking caretaker acknowledgement. Automatic escalation triggers in 60s if unacknowledged.</p>
                    </div>
                </div>

                <div className="mt-8 pt-4 border-t border-slate-100 text-center">
                    <p className="text-xs text-slate-400 font-medium italic">
                        *Demo emergency escalation: Real healthcare/hospital APIs are safely simulated in this demo environment.
                    </p>
                </div>
            </Card>
        </div>
    );
}
