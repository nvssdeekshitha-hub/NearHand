import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { useCare } from '../../context/CareContext';
import { EmergencyStatusTracker } from '../../components/emergency/EmergencyStatusTracker';

export function SeniorEmergency() {
    const navigate = useNavigate();
    const { cancelEmergencySOS } = useCare();

    const handleDeactivate = () => {
        cancelEmergencySOS();
        navigate('/senior');
    };

    return (
        <div className="max-w-3xl mx-auto space-y-6 pb-24 pt-2 animate-fade-in">
            <div>
                <button 
                    onClick={() => navigate('/senior')}
                    className="inline-flex items-center text-sm font-semibold text-slate-500 hover:text-sky-600 transition-colors"
                >
                    <ArrowLeft className="w-4 h-4 mr-1.5" /> Back to Dashboard
                </button>
            </div>

            <EmergencyStatusTracker onCancel={handleDeactivate} />
        </div>
    );
}
