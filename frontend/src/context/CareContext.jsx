import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { api } from '../services/api';
import { mockSeniors, mockUsers, mockAdditionalCaretakers } from '../mock-data/users';

const CareContext = createContext();

export const CareProvider = ({ children }) => {
    const [requests, setRequests] = useState([]);
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);

    // Emergency SOS State
    const [emergencySOS, setEmergencySOS] = useState({
        active: false,
        triggeredAt: null,
        seniorName: 'Lakshmi',
        location: 'Home, Vijayawada',
        timeline: []
    });

    // Location Safety State
    const [locationSafety, setLocationSafety] = useState({
        deviationDetected: true,
        home: 'Vijayawada (Moghalrajpuram)',
        currentLocation: '2.8 km away (MG Road Junction)',
        status: 'Location deviation detected',
        expected: null, // null, true, false
        notifiedCaretaker: true
    });

    // Caretaker status
    const [caretakerStatus, setCaretakerStatus] = useState('Available');

    // Fetch initial data
    const refreshData = useCallback(async () => {
        try {
            setLoading(true);
            const reqs = await api.getRequests('all');
            const notifs = await api.getNotifications();
            setRequests(reqs);
            setNotifications(notifs);
        } catch (err) {
            console.error('Failed to load initial care data:', err);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        refreshData();
    }, [refreshData]);

    // Active vs History separation
    const activeRequests = requests.filter(r =>
        ['CREATED', 'ANALYZING', 'CARETAKER_NOTIFIED', 'WAITING_FOR_RESPONSE', 'ACCEPTED', 'IN_PROGRESS', 'ESCALATED'].includes(r.status)
    );

    const historyRequests = requests.filter(r =>
        ['RESOLVED', 'CANCELLED', 'EXPIRED'].includes(r.status)
    );

    // Filtered lists
    const volunteerEligibleRequests = requests.filter(r => r.status === 'ESCALATED');
    const volunteerActiveAssistance = requests.filter(r => r.status === 'IN_PROGRESS' && r.assigned_volunteer_id === 301);

    // Countdown timer for active requests in WAITING_FOR_RESPONSE
    useEffect(() => {
        const interval = setInterval(() => {
            setRequests(prevRequests => {
                let hasChanges = false;
                const updated = prevRequests.map(req => {
                    if (req.status === 'WAITING_FOR_RESPONSE' && req.seconds_remaining > 0) {
                        hasChanges = true;
                        const nextSec = req.seconds_remaining - 1;
                        if (nextSec <= 0) {
                            // Automatically escalate on timeout!
                            return {
                                ...req,
                                seconds_remaining: 0,
                                status: 'ESCALATED',
                                timeline: [
                                    ...req.timeline,
                                    { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), label: 'Caretaker response window expired', status: 'warning' },
                                    { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), label: 'Escalated to nearby volunteer network', status: 'active' }
                                ]
                            };
                        }
                        return { ...req, seconds_remaining: nextSec };
                    }
                    return req;
                });

                return hasChanges ? updated : prevRequests;
            });
        }, 1000);

        return () => clearInterval(interval);
    }, []);

    // Actions
    const submitSeniorRequest = async ({
        transcript,
        language = 'Telugu',
        request_type = 'Fall',
        category = 'Emergency',
        urgency = 'CRITICAL',
        risk_score = 94,
        target_response_seconds = 120,
        ai_summary = 'Fall / Unable to stand',
        ai_explanation = 'The request indicates a fall and inability to stand.'
    }) => {
        const newReq = await api.createRequest({
            senior_id: 101,
            senior_name: 'Lakshmi',
            senior_age: 72,
            location: 'Home, Vijayawada',
            request_type,
            category,
            urgency,
            risk_score,
            target_response_seconds,
            seconds_remaining: target_response_seconds,
            status: 'WAITING_FOR_RESPONSE',
            language,
            transcript,
            ai_summary,
            ai_explanation
        });

        await refreshData();
        return newReq;
    };

    const caretakerAccept = async (requestId) => {
        const updated = await api.acceptRequest(requestId);
        await refreshData();
        return updated;
    };

    const caretakerTimeout = async (requestId) => {
        const updated = await api.escalateRequest(requestId);
        await refreshData();
        return updated;
    };

    const volunteerAccept = async (requestId) => {
        const updated = await api.volunteerAcceptRequest(requestId, 301);
        await refreshData();
        return updated;
    };

    const resolveRequest = async (requestId, notes = 'Assistance provided successfully.') => {
        const updated = await api.resolveRequest(requestId, notes);
        await refreshData();
        return updated;
    };

    const activateEmergencySOS = () => {
        const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        setEmergencySOS({
            active: true,
            triggeredAt: now,
            seniorName: 'Lakshmi',
            location: 'Home, Vijayawada',
            timeline: [
                { time: now, label: '🚨 Emergency SOS triggered by Lakshmi', status: 'done' },
                { time: now, label: 'Caretaker Ravi Kumar alerted via priority call', status: 'done' },
                { time: now, label: 'Family member Anjali notified', status: 'done' },
                { time: now, label: 'Demo emergency escalation pathway active', status: 'active' }
            ]
        });

        // Also create a high priority request
        submitSeniorRequest({
            transcript: 'EMERGENCY SOS BUTTON ACTIVATED',
            language: 'English',
            request_type: 'Emergency SOS',
            category: 'Emergency',
            urgency: 'CRITICAL',
            risk_score: 99,
            target_response_seconds: 60,
            ai_summary: 'Manual Emergency SOS Activated',
            ai_explanation: 'Senior pressed the prominent SOS button. Immediate response requested.'
        });
    };

    const cancelEmergencySOS = () => {
        setEmergencySOS({
            active: false,
            triggeredAt: null,
            seniorName: 'Lakshmi',
            location: 'Home, Vijayawada',
            timeline: []
        });
    };

    const confirmLocationTrip = async (isExpected) => {
        setLocationSafety(prev => ({
            ...prev,
            expected: isExpected,
            status: isExpected ? 'Expected trip confirmed' : 'Unexpected deviation (Escalated to Care Team)',
            notifiedCaretaker: true
        }));

        if (!isExpected) {
            // Escalate unexpected location deviation
            submitSeniorRequest({
                transcript: 'Unexpected location deviation: Senior is 2.8 km from home',
                language: 'English',
                request_type: 'Location Deviation',
                category: 'Emergency',
                urgency: 'WARNING',
                risk_score: 75,
                target_response_seconds: 300,
                ai_summary: 'Unexpected Location Deviation (2.8 km)',
                ai_explanation: 'Senior left safe perimeter and confirmed the trip was unexpected or unassisted.'
            });
        }
    };

    const requestCompanionship = async (seniorId = 101, notes = '') => {
        const req = await api.sendCompanionshipRequest(seniorId, notes);
        await refreshData();
        return req;
    };

    const requestAdditionalSupport = async (seniorId, caretakerDetails) => {
        const res = await api.sendAdditionalSupportRequest(seniorId, 201, caretakerDetails);
        await refreshData();
        return res;
    };

    const markNotificationRead = async (id) => {
        await api.markNotificationRead(id);
        setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
    };

    const markAllNotificationsRead = async () => {
        await api.markAllNotificationsRead();
        setNotifications(prev => prev.map(n => ({ ...n, read: true })));
    };

    // Reset whole scenario for hackathon demo
    const resetDemoScenario = async () => {
        await api.resetDemoData();
        cancelEmergencySOS();
        setLocationSafety({
            deviationDetected: true,
            home: 'Vijayawada (Moghalrajpuram)',
            currentLocation: '2.8 km away (MG Road Junction)',
            status: 'Location deviation detected',
            expected: null,
            notifiedCaretaker: true
        });
        setCaretakerStatus('Available');
        await refreshData();
    };

    const unreadNotificationCount = notifications.filter(n => !n.read).length;

    return (
        <CareContext.Provider value={{
            requests,
            activeRequests,
            historyRequests,
            volunteerEligibleRequests,
            volunteerActiveAssistance,
            seniors: mockSeniors,
            volunteers: [mockUsers.volunteer],
            caretakers: [mockUsers.caretaker, ...mockAdditionalCaretakers],
            notifications,
            unreadNotificationCount,
            emergencySOS,
            locationSafety,
            caretakerStatus,
            setCaretakerStatus,
            loading,
            // Actions
            submitSeniorRequest,
            caretakerAccept,
            caretakerTimeout,
            volunteerAccept,
            resolveRequest,
            activateEmergencySOS,
            cancelEmergencySOS,
            confirmLocationTrip,
            requestCompanionship,
            requestAdditionalSupport,
            markNotificationRead,
            markAllNotificationsRead,
            resetDemoScenario,
            refreshData
        }}>
            {children}
        </CareContext.Provider>
    );
};

export const useCare = () => {
    const context = useContext(CareContext);
    if (!context) {
        throw new Error('useCare must be used within a CareProvider');
    }
    return context;
};
