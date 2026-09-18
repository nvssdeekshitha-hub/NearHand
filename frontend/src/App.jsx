import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { CareProvider } from './context/CareContext';
import { DemoControls } from './components/shared/DemoControls';

// Layouts
import { PublicLayout } from './layouts/PublicLayout';
import { DashboardLayout } from './layouts/DashboardLayout';

// Pages
import { LandingPage } from './pages/public/LandingPage';
import { LoginPage } from './pages/public/LoginPage';

import { SeniorDashboard } from './pages/senior/SeniorDashboard';
import { SeniorRequest } from './pages/senior/SeniorRequest';
import { SeniorEmergency } from './pages/senior/SeniorEmergency';

import { CaretakerDashboard } from './pages/caretaker/CaretakerDashboard';
import { CaretakerRequests } from './pages/caretaker/CaretakerRequests';
import { CaretakerSeniors } from './pages/caretaker/CaretakerSeniors';
import { CaretakerSeniorDetail } from './pages/caretaker/CaretakerSeniorDetail';

import { VolunteerDashboard } from './pages/volunteer/VolunteerDashboard';
import { FamilyDashboard } from './pages/family/FamilyDashboard';
import { LiveResponseMonitor } from './pages/shared/LiveResponseMonitor';
import { RequestHistoryPage } from './pages/shared/RequestHistoryPage';
import { NotificationsPage } from './pages/shared/NotificationsPage';

export default function App() {
    return (
        <AuthProvider>
            <CareProvider>
                <BrowserRouter>
                    <Routes>
                        {/* Public */}
                        <Route element={<PublicLayout />}>
                            <Route path="/" element={<LandingPage />} />
                            <Route path="/login" element={<LoginPage />} />
                        </Route>

                        {/* Protected Healthcare Dashboards */}
                        <Route element={<DashboardLayout />}>
                            {/* Senior */}
                            <Route path="/senior" element={<SeniorDashboard />} />
                            <Route path="/senior/request" element={<SeniorRequest />} />
                            <Route path="/senior/emergency" element={<SeniorEmergency />} />

                            {/* Caretaker */}
                            <Route path="/caretaker" element={<CaretakerDashboard />} />
                            <Route path="/caretaker/seniors" element={<CaretakerSeniors />} />
                            <Route path="/caretaker/requests" element={<CaretakerRequests />} />
                            <Route path="/caretaker/senior/:id" element={<CaretakerSeniorDetail />} />

                            {/* Volunteer */}
                            <Route path="/volunteer" element={<VolunteerDashboard />} />
                            <Route path="/volunteer/requests" element={<VolunteerDashboard />} />

                            {/* Family */}
                            <Route path="/family" element={<FamilyDashboard />} />
                            <Route path="/family/senior/:id" element={<FamilyDashboard />} />

                            {/* Shared Care Coordination Views */}
                            <Route path="/request/:id" element={<LiveResponseMonitor />} />
                            <Route path="/history" element={<RequestHistoryPage />} />
                            <Route path="/notifications" element={<NotificationsPage />} />
                        </Route>

                        <Route path="*" element={
                            <div className="min-h-screen flex flex-col items-center justify-center p-8 text-center bg-slate-50">
                                <h1 className="text-4xl font-black text-slate-900 mb-2">404</h1>
                                <p className="text-slate-500 mb-6 font-medium">Page not found in NEARHAND Care Platform</p>
                                <a href="/" className="btn-primary text-sm font-bold">Return Home</a>
                            </div>
                        } />
                    </Routes>

                    {/* Global Interactive Demo Simulator Bar */}
                    <DemoControls />
                </BrowserRouter>
            </CareProvider>
        </AuthProvider>
    );
}
