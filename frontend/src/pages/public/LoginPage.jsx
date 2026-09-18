import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { HeartPulse, UserCircle2, Activity, ShieldPlus, Heart, ArrowRight } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { Card } from '../../components/ui/Card';

export function LoginPage() {
    const { login } = useAuth();
    const navigate = useNavigate();
    const [loadingRole, setLoadingRole] = useState(null);

    const handleLogin = async (role) => {
        setLoadingRole(role);
        await login(role);

        if (role === 'senior') navigate('/senior');
        else if (role === 'caretaker') navigate('/caretaker');
        else if (role === 'volunteer') navigate('/volunteer');
        else if (role === 'family') navigate('/family');
    };

    const roles = [
        { 
            id: 'senior', 
            name: 'Senior Citizen', 
            persona: 'Lakshmi, 72', 
            desc: 'Voice request, prominent SOS, today\'s care tracker',
            icon: UserCircle2, 
            color: 'text-sky-600', 
            bg: 'bg-sky-50' 
        },
        { 
            id: 'caretaker', 
            name: 'Primary Caretaker', 
            persona: 'Ravi Kumar', 
            desc: 'Incident response hub, active timers, co-dispatch',
            icon: Activity, 
            color: 'text-emerald-600', 
            bg: 'bg-emerald-50' 
        },
        { 
            id: 'volunteer', 
            name: 'Volunteer Network', 
            persona: 'Priya Sharma (2.4 km)', 
            desc: 'Nearby escalated requests, privacy locks, ETA dispatch',
            icon: ShieldPlus, 
            color: 'text-amber-600', 
            bg: 'bg-amber-50' 
        },
        { 
            id: 'family', 
            name: 'Family Member', 
            persona: 'Anjali (Daughter)', 
            desc: 'Routine wellness, location safety monitor, timeline',
            icon: Heart, 
            color: 'text-rose-600', 
            bg: 'bg-rose-50' 
        },
    ];

    return (
        <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8 animate-fade-in">
            <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
                <div className="w-14 h-14 bg-sky-50 text-sky-600 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-sky-200">
                    <HeartPulse className="w-8 h-8" />
                </div>
                <h2 className="text-3xl font-black text-slate-900 tracking-tight">
                    Sign in to NEARHAND
                </h2>
                <p className="mt-1 text-sm text-slate-500 font-medium">
                    Select a persona to experience the interactive hackathon demo
                </p>
            </div>

            <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-2xl">
                <Card className="p-6 sm:p-8 border-slate-200 shadow-lg">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {roles.map((role) => {
                            const Icon = role.icon;
                            return (
                                <button
                                    key={role.id}
                                    onClick={() => handleLogin(role.id)}
                                    disabled={loadingRole !== null}
                                    className="flex flex-col text-left p-5 border border-slate-200 rounded-2xl hover:border-sky-400 hover:shadow-md transition-all group bg-white cursor-pointer"
                                >
                                    <div className="flex items-center space-x-3 mb-3">
                                        <div className={`p-3 rounded-xl ${role.bg} ${role.color} group-hover:scale-105 transition-transform`}>
                                            <Icon className="w-6 h-6" />
                                        </div>
                                        <div>
                                            <h3 className="text-base font-bold text-slate-900 group-hover:text-sky-600 transition-colors">
                                                {role.name}
                                            </h3>
                                            <span className="text-xs font-semibold text-slate-500">
                                                {role.persona}
                                            </span>
                                        </div>
                                    </div>
                                    <p className="text-xs text-slate-500 leading-relaxed font-medium">
                                        {role.desc}
                                    </p>
                                    <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-xs font-bold text-sky-600 group-hover:text-sky-700">
                                        <span>{loadingRole === role.id ? 'Authenticating...' : 'Enter Dashboard'}</span>
                                        <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                                    </div>
                                </button>
                            );
                        })}
                    </div>
                </Card>

                <div className="text-center mt-6">
                    <button
                        onClick={() => navigate('/')}
                        className="text-xs text-slate-400 hover:text-slate-600 font-semibold"
                    >
                        ← Back to Landing Page
                    </button>
                </div>
            </div>
        </div>
    );
}
