import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bell, CheckCircle2, ShieldAlert, Zap, Pill, Heart, UserCheck, AlertTriangle } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { useCare } from '../../context/CareContext';

export function NotificationsPage() {
    const navigate = useNavigate();
    const { notifications, markNotificationRead, markAllNotificationsRead } = useCare();
    const [filter, setFilter] = useState('all'); // 'all' | 'unread'

    const filtered = notifications.filter(n => filter === 'all' || !n.read);

    const getIcon = (type, title) => {
        if (title?.includes('Critical') || type === 'critical') {
            return <ShieldAlert className="w-5 h-5 text-rose-600" />;
        }
        if (title?.includes('timeout') || title?.includes('Timeout')) {
            return <Zap className="w-5 h-5 text-amber-500" />;
        }
        if (title?.includes('Medication') || title?.includes('pill')) {
            return <Pill className="w-5 h-5 text-indigo-500" />;
        }
        if (title?.includes('Companionship') || title?.includes('Company')) {
            return <Heart className="w-5 h-5 text-sky-500" />;
        }
        if (title?.includes('Volunteer') || title?.includes('Priya')) {
            return <UserCheck className="w-5 h-5 text-emerald-600" />;
        }
        if (type === 'warning') {
            return <AlertTriangle className="w-5 h-5 text-amber-500" />;
        }
        return <CheckCircle2 className="w-5 h-5 text-emerald-500" />;
    };

    const handleClick = (notif) => {
        markNotificationRead(notif.id);
        if (notif.requestId) {
            navigate(`/request/${notif.requestId}`);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6 pb-20 animate-fade-in">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
                <div>
                    <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight flex items-center">
                        <Bell className="w-7 h-7 text-sky-600 mr-2.5" /> Notification Center
                    </h1>
                    <p className="text-slate-500 font-medium text-sm mt-0.5">
                        Priority care events, escalation alerts, and family communications.
                    </p>
                </div>

                <div className="flex items-center space-x-2">
                    <Button 
                        size="sm" 
                        variant="secondary"
                        onClick={markAllNotificationsRead}
                        className="text-xs font-semibold"
                    >
                        Mark All Read
                    </Button>
                </div>
            </div>

            {/* Filter Pills */}
            <div className="flex space-x-2">
                <button
                    onClick={() => setFilter('all')}
                    className={`px-4 py-1.5 rounded-xl text-xs font-bold transition-colors ${
                        filter === 'all'
                            ? 'bg-sky-600 text-white shadow-xs'
                            : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
                    }`}
                >
                    All Notifications ({notifications.length})
                </button>
                <button
                    onClick={() => setFilter('unread')}
                    className={`px-4 py-1.5 rounded-xl text-xs font-bold transition-colors ${
                        filter === 'unread'
                            ? 'bg-sky-600 text-white shadow-xs'
                            : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
                    }`}
                >
                    Unread ({notifications.filter(n => !n.read).length})
                </button>
            </div>

            {/* Notifications Feed */}
            {filtered.length === 0 ? (
                <Card className="p-16 text-center border-dashed border-2 border-slate-200">
                    <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto mb-3 opacity-70" />
                    <h3 className="text-lg font-bold text-slate-800">All notifications caught up</h3>
                    <p className="text-sm text-slate-500 mt-1">No alerts waiting in this view.</p>
                </Card>
            ) : (
                <div className="space-y-3">
                    {filtered.map(notif => (
                        <Card
                            key={notif.id}
                            onClick={() => handleClick(notif)}
                            className={`p-4 sm:p-5 transition-all cursor-pointer flex items-start space-x-4 ${
                                notif.read 
                                    ? 'border-slate-200 hover:border-slate-300 bg-white' 
                                    : 'border-sky-300 bg-sky-50/40 shadow-xs'
                            }`}
                        >
                            <div className="p-2.5 bg-white rounded-2xl shadow-xs border border-slate-100 shrink-0">
                                {getIcon(notif.type, notif.title)}
                            </div>

                            <div className="flex-1 min-w-0">
                                <div className="flex items-center justify-between">
                                    <h4 className={`text-sm font-bold ${notif.read ? 'text-slate-800' : 'text-slate-900'}`}>
                                        {notif.title}
                                    </h4>
                                    <span className="text-[11px] text-slate-400 font-medium shrink-0 ml-2">
                                        {notif.timestamp}
                                    </span>
                                </div>
                                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                                    {notif.message}
                                </p>
                            </div>

                            {!notif.read && (
                                <span className="w-2.5 h-2.5 rounded-full bg-sky-500 shrink-0 self-center"></span>
                            )}
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
}
