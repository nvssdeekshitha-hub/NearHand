import React, { useState } from 'react';
import { 
    History, 
    Search 
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { useCare } from '../../context/CareContext';

export function RequestHistoryPage() {
    const { historyRequests, activeRequests } = useCare();
    const [selectedCategory, setSelectedCategory] = useState('All');
    const [searchTerm, setSearchTerm] = useState('');

    const categories = ['All', 'Emergency', 'Medical', 'Medication', 'Companionship', 'Assistance'];

    const filtered = historyRequests.filter(req => {
        const matchesCat = selectedCategory === 'All' || 
            req.category?.toLowerCase() === selectedCategory.toLowerCase() ||
            req.request_type?.toLowerCase() === selectedCategory.toLowerCase();
        const matchesSearch = !searchTerm || 
            req.senior_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            req.ai_summary?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            req.id?.toLowerCase().includes(searchTerm.toLowerCase());
        return matchesCat && matchesSearch;
    });

    return (
        <div className="max-w-6xl mx-auto space-y-6 pb-20 animate-fade-in">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
                <div>
                    <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight flex items-center">
                        <History className="w-7 h-7 text-sky-600 mr-2.5" /> Request History
                    </h1>
                    <p className="text-slate-500 font-medium text-sm mt-0.5">
                        Archived and resolved requests. Active queue items are kept separate.
                    </p>
                </div>

                <div className="flex items-center space-x-3">
                    <span className="text-xs text-slate-500 font-bold bg-slate-100 px-3 py-1.5 rounded-xl border border-slate-200">
                        {activeRequests.length} Active • {historyRequests.length} Archived
                    </span>
                </div>
            </div>

            {/* Filter Bar */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="flex flex-wrap gap-2 w-full sm:w-auto">
                    {categories.map(cat => (
                        <button
                            key={cat}
                            onClick={() => setSelectedCategory(cat)}
                            className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-colors ${
                                selectedCategory === cat
                                    ? 'bg-sky-600 text-white shadow-xs'
                                    : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
                            }`}
                        >
                            {cat}
                        </button>
                    ))}
                </div>

                <div className="relative w-full sm:w-64">
                    <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                    <input
                        type="text"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        placeholder="Search history records..."
                        className="w-full pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-sky-500"
                    />
                </div>
            </div>

            {/* Results Table (Desktop) & Cards (Mobile) */}
            {filtered.length === 0 ? (
                <Card className="p-16 text-center border-dashed border-2 border-slate-200">
                    <History className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                    <h3 className="text-lg font-bold text-slate-800">No matching history records</h3>
                    <p className="text-sm text-slate-500 mt-1">Try selecting a different filter category or search term.</p>
                </Card>
            ) : (
                <>
                    {/* Desktop Table (Part 34) */}
                    <div className="hidden md:block bg-white rounded-3xl border border-slate-200 shadow-xs overflow-hidden">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-slate-50/80 border-b border-slate-200 text-slate-400 text-[11px] font-bold uppercase tracking-wider">
                                <tr>
                                    <th className="py-3.5 px-5">Incident ID</th>
                                    <th className="py-3.5 px-5">Senior</th>
                                    <th className="py-3.5 px-5">Category / Summary</th>
                                    <th className="py-3.5 px-5">Urgency</th>
                                    <th className="py-3.5 px-5">Responder</th>
                                    <th className="py-3.5 px-5">Resolution Notes</th>
                                    <th className="py-3.5 px-5 text-right">Status</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {filtered.map(req => (
                                    <tr key={req.id} className="hover:bg-slate-50/80 transition-colors">
                                        <td className="py-4 px-5 font-mono text-xs font-bold text-slate-500">
                                            #{req.id}
                                        </td>
                                        <td className="py-4 px-5 font-bold text-slate-900">
                                            {req.senior_name}, {req.senior_age}
                                        </td>
                                        <td className="py-4 px-5">
                                            <p className="font-semibold text-slate-800">{req.ai_summary}</p>
                                            <span className="text-[11px] text-slate-400">{req.category}</span>
                                        </td>
                                        <td className="py-4 px-5">
                                            <Badge variant={req.urgency === 'CRITICAL' ? 'critical' : req.urgency === 'WARNING' ? 'warning' : 'gray'}>
                                                {req.urgency}
                                            </Badge>
                                        </td>
                                        <td className="py-4 px-5 text-xs text-slate-600 font-medium">
                                            {req.assigned_volunteer_name ? (
                                                <span className="font-bold text-emerald-700">Volunteer {req.assigned_volunteer_name}</span>
                                            ) : (
                                                <span>Caretaker {req.assigned_caretaker_name || 'Ravi Kumar'}</span>
                                            )}
                                        </td>
                                        <td className="py-4 px-5 text-xs text-slate-600 max-w-xs truncate font-medium">
                                            {req.resolution_notes || 'Resolved on scene'}
                                        </td>
                                        <td className="py-4 px-5 text-right">
                                            <span className="inline-flex items-center text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                                                ✓ {req.status}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {/* Mobile Cards View */}
                    <div className="md:hidden space-y-3">
                        {filtered.map(req => (
                            <Card key={req.id} className="p-4 border-slate-200 space-y-2 text-xs">
                                <div className="flex items-center justify-between">
                                    <span className="font-mono text-slate-400 font-bold">#{req.id}</span>
                                    <Badge variant={req.urgency === 'CRITICAL' ? 'critical' : 'warning'}>
                                        {req.urgency}
                                    </Badge>
                                </div>
                                <h4 className="font-black text-sm text-slate-900">{req.senior_name}, {req.senior_age}</h4>
                                <p className="font-bold text-slate-800">{req.ai_summary}</p>
                                <p className="text-slate-600 italic">Notes: {req.resolution_notes || 'Resolved on scene'}</p>
                                <div className="flex items-center justify-between pt-2 border-t border-slate-100 text-slate-400">
                                    <span>{req.assigned_volunteer_name ? `Volunteer ${req.assigned_volunteer_name}` : 'Caretaker Ravi'}</span>
                                    <span className="font-bold text-emerald-600">✓ {req.status}</span>
                                </div>
                            </Card>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
}
