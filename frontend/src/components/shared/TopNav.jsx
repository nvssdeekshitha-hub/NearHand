import React, { useState } from 'react';
import { HeartPulse, Bell, UserCircle2, ChevronDown, LogOut, Shield, Users, Heart } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useCare } from '../../context/CareContext';
import { NotificationDrawer } from './NotificationDrawer';

export function TopNav({ user, onToggleMobileMenu }) {
    const { logout, login } = useAuth();
    const { unreadNotificationCount } = useCare();
    const navigate = useNavigate();
    const [isNotifOpen, setIsNotifOpen] = useState(false);
    const [roleMenuOpen, setRoleMenuOpen] = useState(false);

    const isSenior = user?.role === 'senior';

    const switchRole = async (targetRole, targetPath) => {
        setRoleMenuOpen(false);
        await login(targetRole);
        navigate(targetPath);
    };

    return (
        <>
            <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-xs">
                <div className="flex items-center justify-between px-4 sm:px-6 lg:px-8 h-16 max-w-7xl mx-auto w-full">
                    
                    {/* Brand */}
                    <div className="flex items-center space-x-3">
                        {!isSenior && onToggleMobileMenu && (
                            <button 
                                onClick={onToggleMobileMenu}
                                className="md:hidden p-2 -ml-2 mr-1 text-slate-500 hover:text-slate-800 rounded-lg hover:bg-slate-100"
                                aria-label="Toggle navigation menu"
                            >
                                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                                </svg>
                            </button>
                        )}
                        <Link to={isSenior ? '/senior' : `/${user?.role || ''}`} className="flex items-center space-x-2.5 group">
                            <div className="w-9 h-9 rounded-xl bg-sky-50 flex items-center justify-center border border-sky-100 group-hover:scale-105 transition-transform">
                                <HeartPulse className="w-5 h-5 text-sky-600" />
                            </div>
                            <span className="font-extrabold text-xl text-slate-900 tracking-tight">NEARHAND</span>
                        </Link>
                    </div>

                    {/* Right Controls */}
                    <div className="flex items-center space-x-3 sm:space-x-4">
                        
                        {/* Quick Demo Role Switcher */}
                        <div className="relative">
                            <button
                                onClick={() => setRoleMenuOpen(!roleMenuOpen)}
                                className="flex items-center space-x-2 px-3 py-1.5 rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100 text-xs font-semibold text-slate-700 transition-colors"
                                title="Quick Role Switcher for Demos"
                            >
                                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                <span className="capitalize">{user?.role || 'Guest'}</span>
                                <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                            </button>

                            {roleMenuOpen && (
                                <div className="absolute right-0 mt-2 w-52 bg-white rounded-2xl shadow-xl border border-slate-100 py-2 z-50 animate-fade-in text-xs">
                                    <div className="px-3 py-1.5 text-[10px] font-bold text-slate-400 uppercase tracking-wider border-b border-slate-100 mb-1">
                                        Switch Role View
                                    </div>
                                    <button
                                        onClick={() => switchRole('senior', '/senior')}
                                        className="w-full text-left px-3 py-2 flex items-center hover:bg-sky-50 text-slate-700 font-medium"
                                    >
                                        <UserCircle2 className="w-4 h-4 mr-2 text-sky-600" /> Senior (Lakshmi)
                                    </button>
                                    <button
                                        onClick={() => switchRole('caretaker', '/caretaker')}
                                        className="w-full text-left px-3 py-2 flex items-center hover:bg-emerald-50 text-slate-700 font-medium"
                                    >
                                        <Shield className="w-4 h-4 mr-2 text-emerald-600" /> Caretaker (Ravi Kumar)
                                    </button>
                                    <button
                                        onClick={() => switchRole('volunteer', '/volunteer')}
                                        className="w-full text-left px-3 py-2 flex items-center hover:bg-amber-50 text-slate-700 font-medium"
                                    >
                                        <Users className="w-4 h-4 mr-2 text-amber-600" /> Volunteer (Priya Sharma)
                                    </button>
                                    <button
                                        onClick={() => switchRole('family', '/family')}
                                        className="w-full text-left px-3 py-2 flex items-center hover:bg-rose-50 text-slate-700 font-medium"
                                    >
                                        <Heart className="w-4 h-4 mr-2 text-rose-500" /> Family (Anjali)
                                    </button>
                                </div>
                            )}
                        </div>

                        {/* Notifications Bell */}
                        <button
                            onClick={() => setIsNotifOpen(true)}
                            className="p-2 text-slate-600 hover:text-slate-900 rounded-xl hover:bg-slate-100 relative transition-colors"
                            aria-label="View notifications"
                        >
                            <Bell className="w-5 h-5" />
                            {unreadNotificationCount > 0 && (
                                <span className="absolute top-1 right-1 w-4 h-4 bg-rose-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                                    {unreadNotificationCount}
                                </span>
                            )}
                        </button>

                        {/* User Profile Badge & Logout */}
                        <div className="flex items-center space-x-2 pl-2 border-l border-slate-200">
                            <div className="hidden sm:flex flex-col text-right">
                                <span className="text-xs font-bold text-slate-900 leading-tight">{user?.name}</span>
                                <span className="text-[10px] text-slate-400 capitalize">{user?.role}</span>
                            </div>
                            <button
                                onClick={logout}
                                className="p-2 text-slate-400 hover:text-slate-700 rounded-xl hover:bg-slate-100 transition-colors"
                                title="Sign Out"
                            >
                                <LogOut className="w-4 h-4" />
                            </button>
                        </div>

                    </div>
                </div>
            </header>

            <NotificationDrawer isOpen={isNotifOpen} onClose={() => setIsNotifOpen(false)} />
        </>
    );
}
