import React from 'react';
import { useNavigate } from 'react-router-dom';
import { X, Bell, ShieldAlert, AlertTriangle, CheckCircle2, Zap, Heart, Pill, UserCheck } from 'lucide-react';
import { useCare } from '../../context/CareContext';

export function NotificationDrawer({ isOpen, onClose }) {
    const { notifications, markNotificationRead, markAllNotificationsRead } = useCare();
    const navigate = useNavigate();

    if (!isOpen) return null;

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

    const handleNotificationClick = (notif) => {
        markNotificationRead(notif.id);
        onClose();
        if (notif.requestId) {
            navigate(`/request/${notif.requestId}`);
        }
    };

    return (
        <div className="fixed inset-0 z-50 overflow-hidden animate-fade-in">
            <div 
                className="absolute inset-0 bg-slate-900/40 backdrop-blur-xs transition-opacity" 
                onClick={onClose} 
            />

            <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
                <div className="w-screen max-w-md bg-white shadow-2xl flex flex-col border-l border-slate-100">
                    
                    {/* Header */}
                    <div className="px-6 py-5 border-b border-slate-100 flex items-center justify-between">
                        <div className="flex items-center space-x-2.5">
                            <Bell className="w-5 h-5 text-sky-600" />
                            <h2 className="text-lg font-bold text-slate-900">Notifications</h2>
                            <span className="text-xs bg-sky-100 text-sky-700 font-bold px-2 py-0.5 rounded-full">
                                {notifications.length}
                            </span>
                        </div>
                        <div className="flex items-center space-x-2">
                            <button 
                                onClick={markAllNotificationsRead}
                                className="text-xs text-sky-600 hover:text-sky-800 font-semibold px-2 py-1 rounded hover:bg-sky-50 transition-colors"
                            >
                                Mark all read
                            </button>
                            <button 
                                onClick={onClose}
                                className="p-1 rounded-full text-slate-400 hover:text-slate-600 hover:bg-slate-100"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>
                    </div>

                    {/* Notifications List */}
                    <div className="flex-1 overflow-y-auto divide-y divide-slate-100 p-2">
                        {notifications.length === 0 ? (
                            <div className="text-center py-16 text-slate-400">
                                <Bell className="w-12 h-12 mx-auto mb-3 opacity-30" />
                                <p className="font-semibold text-sm">No notifications yet</p>
                            </div>
                        ) : (
                            notifications.map(notif => (
                                <div
                                    key={notif.id}
                                    onClick={() => handleNotificationClick(notif)}
                                    className={`p-4 rounded-2xl transition-colors cursor-pointer flex items-start space-x-3.5 ${
                                        notif.read ? 'hover:bg-slate-50 bg-white' : 'bg-sky-50/50 hover:bg-sky-50/80 border border-sky-100/60'
                                    }`}
                                >
                                    <div className="p-2 bg-white rounded-xl shadow-xs border border-slate-100 shrink-0 mt-0.5">
                                        {getIcon(notif.type, notif.title)}
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center justify-between">
                                            <p className={`text-sm font-bold truncate ${notif.read ? 'text-slate-800' : 'text-slate-900'}`}>
                                                {notif.title}
                                            </p>
                                            <span className="text-[11px] text-slate-400 shrink-0 ml-2">
                                                {notif.timestamp}
                                            </span>
                                        </div>
                                        <p className="text-xs text-slate-600 mt-1 leading-relaxed line-clamp-2">
                                            {notif.message}
                                        </p>
                                        {!notif.read && (
                                            <span className="inline-block w-2 h-2 rounded-full bg-sky-500 mt-2"></span>
                                        )}
                                    </div>
                                </div>
                            ))
                        )}
                    </div>

                </div>
            </div>
        </div>
    );
}
