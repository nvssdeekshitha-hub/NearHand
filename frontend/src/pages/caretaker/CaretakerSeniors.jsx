import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Users, MapPin, Pill, ArrowLeft, Activity } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { useCare } from '../../context/CareContext';

export function CaretakerSeniors() {
    const navigate = useNavigate();
    const { seniors, activeRequests } = useCare();
    const [searchTerm, setSearchTerm] = useState('');

    const filtered = seniors.filter(s => 
        s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        s.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
        s.conditions?.some(c => c.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    return (
        <div className="max-w-5xl mx-auto space-y-6 pb-20 animate-fade-in">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
                <div>
                    <button 
                        onClick={() => navigate('/caretaker')}
                        className="text-xs font-bold text-slate-500 hover:text-sky-600 flex items-center mb-2"
                    >
                        <ArrowLeft className="w-3.5 h-3.5 mr-1" /> Back to Dashboard
                    </button>
                    <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
                        Assigned Seniors ({seniors.length})
                    </h1>
                </div>

                <div className="relative w-full sm:w-72">
                    <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                    <input
                        type="text"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        placeholder="Search seniors or conditions..."
                        className="w-full pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500"
                    />
                </div>
            </div>

            {/* Seniors Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                {filtered.map(senior => {
                    const activeAlert = activeRequests.find(r => r.senior_id === senior.id);
                    const takenMeds = senior.medications ? senior.medications.filter(m => m.taken).length : 0;
                    const totalMeds = senior.medications ? senior.medications.length : 0;

                    return (
                        <Card 
                            key={senior.id}
                            onClick={() => navigate(`/caretaker/senior/${senior.id}`)}
                            className="p-5 hover:shadow-md transition-all cursor-pointer hover:border-sky-300 border-slate-200 group flex flex-col justify-between"
                        >
                            <div>
                                <div className="flex items-start justify-between mb-3">
                                    <div>
                                        <h3 className="text-xl font-bold text-slate-900 group-hover:text-sky-600 transition-colors">
                                            {senior.name}, {senior.age}
                                        </h3>
                                        <p className="text-xs text-slate-500 flex items-center mt-0.5">
                                            <MapPin className="w-3.5 h-3.5 mr-1 text-slate-400" /> {senior.location}
                                        </p>
                                    </div>
                                    <Badge variant={activeAlert ? (activeAlert.urgency === 'CRITICAL' ? 'critical' : 'warning') : 'success'}>
                                        {activeAlert ? `${activeAlert.urgency} Alert` : 'Stable'}
                                    </Badge>
                                </div>

                                <div className="space-y-2 py-2 text-xs text-slate-600 border-t border-slate-100 mt-2">
                                    <p>
                                        <span className="font-semibold text-slate-400 uppercase text-[10px] block">Conditions</span>
                                        <span className="font-medium text-slate-800">
                                            {senior.conditions?.join(', ') || 'None recorded'}
                                        </span>
                                    </p>
                                    <p>
                                        <span className="font-semibold text-slate-400 uppercase text-[10px] block">Medications Today</span>
                                        <span className="font-medium text-slate-800 flex items-center mt-0.5">
                                            <Pill className="w-3.5 h-3.5 mr-1 text-emerald-600" />
                                            {totalMeds > 0 ? `${takenMeds} / ${totalMeds} Taken` : 'No meds scheduled'}
                                        </span>
                                    </p>
                                </div>
                            </div>

                            <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-bold text-sky-600 group-hover:text-sky-700">
                                <span>View Full Profile</span>
                                <span>→</span>
                            </div>
                        </Card>
                    );
                })}
            </div>
        </div>
    );
}
