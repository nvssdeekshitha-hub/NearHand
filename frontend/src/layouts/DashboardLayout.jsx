import React, { useState } from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Sidebar } from '../components/shared/Sidebar';
import { TopNav } from '../components/shared/TopNav';
import { X, Menu } from 'lucide-react';

export function DashboardLayout() {
    const { user } = useAuth();
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    const isSenior = user?.role === 'senior';

    return (
        <div className="min-h-screen bg-slate-50 flex flex-col">
            <TopNav user={user} onToggleMobileMenu={() => setMobileMenuOpen(!mobileMenuOpen)} />

            <div className="flex flex-1">
                {/* Desktop Sidebar */}
                {!isSenior && (
                    <div className="hidden md:flex w-64 flex-col shrink-0 border-r border-slate-800">
                        <Sidebar role={user.role} />
                    </div>
                )}

                {/* Mobile Drawer */}
                {!isSenior && mobileMenuOpen && (
                    <div className="fixed inset-0 z-50 md:hidden flex animate-fade-in">
                        <div 
                            className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs" 
                            onClick={() => setMobileMenuOpen(false)} 
                        />
                        <div className="relative flex-1 flex flex-col max-w-xs w-full bg-slate-900 z-10">
                            <div className="absolute top-0 right-0 -mr-12 pt-2">
                                <button
                                    onClick={() => setMobileMenuOpen(false)}
                                    className="ml-1 flex items-center justify-center h-10 w-10 rounded-full text-white"
                                >
                                    <X className="h-6 w-6" />
                                </button>
                            </div>
                            <div onClick={() => setMobileMenuOpen(false)} className="h-full">
                                <Sidebar role={user.role} />
                            </div>
                        </div>
                    </div>
                )}

                {/* Main Content Area */}
                <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto w-full">
                    <Outlet />
                </main>
            </div>
        </div>
    );
}
