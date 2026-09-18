import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Users, Activity, History, Bell, HeartPulse } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useCare } from '../../context/CareContext';

export function Sidebar({ role }) {
    const { user } = useAuth();
    const { activeRequests, unreadNotificationCount } = useCare();

    const getLinks = () => {
        switch (role) {
            case 'caretaker':
                return [
                    { name: 'Dashboard', path: '/caretaker', icon: LayoutDashboard },
                    { name: 'My Seniors', path: '/caretaker/seniors', icon: Users },
                    { name: 'Active Requests', path: '/caretaker/requests', icon: Activity, badge: activeRequests.length },
                    { name: 'Request History', path: '/history', icon: History },
                    { name: 'Notifications', path: '/notifications', icon: Bell, badge: unreadNotificationCount },
                ];
            case 'volunteer':
                return [
                    { name: 'Nearby Assistance', path: '/volunteer', icon: HeartPulse },
                    { name: 'Request History', path: '/history', icon: History },
                    { name: 'Notifications', path: '/notifications', icon: Bell, badge: unreadNotificationCount },
                ];
            case 'family':
                return [
                    { name: 'Care Overview', path: '/family', icon: LayoutDashboard },
                    { name: 'Request History', path: '/history', icon: History },
                    { name: 'Notifications', path: '/notifications', icon: Bell, badge: unreadNotificationCount },
                ];
            default:
                return [];
        }
    };

    const links = getLinks();

    return (
        <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col text-white h-full shrink-0">
            {/* Logo */}
            <div className="p-6 flex items-center space-x-3 border-b border-slate-800/80">
                <div className="w-9 h-9 rounded-xl bg-sky-500/10 border border-sky-400/30 flex items-center justify-center">
                    <HeartPulse className="w-5 h-5 text-sky-400" />
                </div>
                <div>
                    <span className="text-lg font-black tracking-tight text-white block">NEARHAND</span>
                    <span className="text-[10px] text-slate-400 font-semibold tracking-wider uppercase block">Care Coordination</span>
                </div>
            </div>

            {/* Nav Links */}
            <nav className="flex-1 px-3 space-y-1.5 py-6 overflow-y-auto">
                {links.map(link => {
                    const Icon = link.icon;
                    return (
                        <NavLink
                            key={link.path + link.name}
                            to={link.path}
                            end={link.path === '/caretaker' || link.path === '/volunteer' || link.path === '/family'}
                            className={({ isActive }) =>
                                `flex items-center justify-between px-3.5 py-2.5 rounded-xl transition-all font-medium text-sm ${
                                    isActive
                                        ? 'bg-sky-600 text-white shadow-sm font-semibold'
                                        : 'text-slate-400 hover:bg-slate-800 hover:text-slate-100'
                                }`
                            }
                        >
                            <div className="flex items-center space-x-3">
                                <Icon className="w-4 h-4" />
                                <span>{link.name}</span>
                            </div>
                            {Boolean(link.badge) && link.badge > 0 && (
                                <span className="text-xs bg-rose-500 text-white font-bold px-2 py-0.5 rounded-full">
                                    {link.badge}
                                </span>
                            )}
                        </NavLink>
                    );
                })}
            </nav>

            {/* Bottom User Card */}
            <div className="p-4 border-t border-slate-800 bg-slate-950/40">
                <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-sm font-bold text-sky-400">
                        {user?.name ? user.name.slice(0, 2).toUpperCase() : 'NH'}
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className="text-xs font-bold text-slate-200 truncate">{user?.name || 'User'}</p>
                        <div className="flex items-center space-x-1.5 mt-0.5">
                            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                            <span className="text-[11px] text-slate-400 capitalize">{user?.role || 'Active'}</span>
                        </div>
                    </div>
                </div>
            </div>
        </aside>
    );
}
