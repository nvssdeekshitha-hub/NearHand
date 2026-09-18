import React, { useState } from 'react';
import { 
    Activity, 
    ShieldAlert, 
    Clock, 
    UserCheck, 
    MapPin, 
    CheckCircle2, 
    RotateCcw, 
    X, 
    Sliders
} from 'lucide-react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { useNavigate } from 'react-router-dom';
import { useCare } from '../../context/CareContext';
import { useAuth } from '../../context/AuthContext';

export function DemoControls() {
    const [isOpen, setIsOpen] = useState(false);
    const { 
        activeRequests, 
        activateEmergencySOS, 
        caretakerTimeout, 
        volunteerAccept, 
        resolveRequest, 
        confirmLocationTrip, 
        resetDemoScenario 
    } = useCare();
    const { login } = useAuth();
    const navigate = useNavigate();

    const targetRequest = activeRequests.find(r => r.senior_name === 'Lakshmi') || activeRequests[0];

    const handleTimeout = async () => {
        if (targetRequest) {
            await caretakerTimeout(targetRequest.id);
            navigate(`/request/${targetRequest.id}`);
        }
    };

    const handleVolunteerAccept = async () => {
        if (targetRequest) {
            await volunteerAccept(targetRequest.id);
            await login('volunteer');
            navigate('/volunteer');
        }
    };

    const handleResolve = async () => {
        if (targetRequest) {
            await resolveRequest(targetRequest.id, 'Volunteer and caretaker ensured senior was safe and stable.');
            navigate('/history');
        }
    };

    const handleReset = async () => {
        await resetDemoScenario();
        setScenarioStep(1);
        navigate('/senior');
    };

    if (!isOpen) {
        return (
            <button
                onClick={() => setIsOpen(true)}
                className="fixed bottom-5 right-5 bg-slate-900 hover:bg-slate-800 text-white p-3.5 rounded-full shadow-2xl z-50 transition-all hover:scale-105 flex items-center space-x-2 border border-slate-700 font-semibold text-xs"
                title="Hackathon Demo Simulation Controls"
            >
                <Sliders className="w-5 h-5 text-sky-400" />
                <span className="hidden sm:inline">Demo Controls</span>
            </button>
        );
    }

    return (
        <div className="fixed bottom-5 right-5 z-50 w-96 max-w-[calc(100vw-2.5rem)] animate-fade-in">
            <Card className="border-sky-500 shadow-2xl bg-white/95 backdrop-blur p-5 border-2">
                {/* Header */}
                <div className="flex justify-between items-center pb-3 border-b border-slate-200 mb-3">
                    <div className="flex items-center space-x-2">
                        <Sliders className="w-4 h-4 text-sky-600" />
                        <h3 className="font-extrabold text-slate-900 text-xs uppercase tracking-wider">
                            Hackathon Demo Controls
                        </h3>
                    </div>
                    <button 
                        onClick={() => setIsOpen(false)} 
                        className="text-slate-400 hover:text-slate-600 p-1 rounded-lg hover:bg-slate-100"
                    >
                        <X className="w-4 h-4" />
                    </button>
                </div>

                {/* Scenario Steps Guidance */}
                <div className="bg-sky-50/70 p-3 rounded-xl border border-sky-100 mb-4 text-xs">
                    <p className="font-bold text-sky-900 mb-1 flex items-center">
                        <Activity className="w-3.5 h-3.5 mr-1 text-sky-600" /> Demo Scenario Flow:
                    </p>
                    <p className="text-slate-600 leading-relaxed">
                        Target: <span className="font-bold text-slate-800">{targetRequest ? targetRequest.id : 'No active request'}</span> ({targetRequest ? targetRequest.status : 'None'})
                    </p>
                </div>

                {/* Simulation Buttons */}
                <div className="space-y-2 text-xs">
                    <Button 
                        variant="secondary" 
                        size="sm"
                        className="w-full justify-start text-left font-semibold border-rose-200 text-rose-700 hover:bg-rose-50"
                        onClick={() => {
                            activateEmergencySOS();
                            navigate('/senior/emergency');
                        }}
                    >
                        <ShieldAlert className="w-4 h-4 mr-2 text-rose-600" /> 1. Simulate Emergency SOS
                    </Button>

                    <Button 
                        variant="secondary" 
                        size="sm"
                        disabled={!targetRequest || targetRequest.status === 'ESCALATED' || targetRequest.status === 'RESOLVED'}
                        className="w-full justify-start text-left font-semibold border-amber-200 text-amber-700 hover:bg-amber-50"
                        onClick={handleTimeout}
                    >
                        <Clock className="w-4 h-4 mr-2 text-amber-500" /> 2. Simulate Caretaker Timeout
                    </Button>

                    <Button 
                        variant="secondary" 
                        size="sm"
                        disabled={!targetRequest || targetRequest.status !== 'ESCALATED'}
                        className="w-full justify-start text-left font-semibold border-emerald-200 text-emerald-700 hover:bg-emerald-50"
                        onClick={handleVolunteerAccept}
                    >
                        <UserCheck className="w-4 h-4 mr-2 text-emerald-600" /> 3. Simulate Volunteer Acceptance
                    </Button>

                    <Button 
                        variant="secondary" 
                        size="sm"
                        className="w-full justify-start text-left font-semibold text-slate-700"
                        onClick={() => {
                            confirmLocationTrip(false);
                            navigate('/family');
                        }}
                    >
                        <MapPin className="w-4 h-4 mr-2 text-indigo-500" /> 4. Simulate Location Deviation
                    </Button>

                    <Button 
                        variant="secondary" 
                        size="sm"
                        disabled={!targetRequest || targetRequest.status === 'RESOLVED'}
                        className="w-full justify-start text-left font-semibold border-teal-200 text-teal-800 hover:bg-teal-50"
                        onClick={handleResolve}
                    >
                        <CheckCircle2 className="w-4 h-4 mr-2 text-teal-600" /> 5. Simulate Request Resolution
                    </Button>
                </div>

                {/* Reset Scenario */}
                <div className="pt-3 mt-3 border-t border-slate-200">
                    <Button 
                        variant="secondary"
                        size="sm"
                        className="w-full justify-center bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold"
                        onClick={handleReset}
                    >
                        <RotateCcw className="w-3.5 h-3.5 mr-1.5 text-slate-600" /> Reset Demo Scenario
                    </Button>
                </div>
            </Card>
        </div>
    );
}
