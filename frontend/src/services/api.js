import { mockUsers, mockSeniors, mockAdditionalCaretakers } from '../mock-data/users';

const BACKEND_URL = import.meta.env.VITE_API_BASE_URL;
const MOCK_DELAY = 400;

const delay = (ms = MOCK_DELAY) => new Promise(resolve => setTimeout(resolve, ms));

// Realistic initial requests collection for demo
const createInitialRequests = () => [
    {
        id: 'REQ-1011',
        senior_id: 101,
        senior_name: 'Lakshmi',
        senior_age: 72,
        location: 'Home, Vijayawada',
        request_type: 'Fall',
        category: 'Emergency',
        urgency: 'CRITICAL',
        risk_score: 94,
        target_response_seconds: 120,
        seconds_remaining: 84,
        status: 'WAITING_FOR_RESPONSE', // CREATED -> ANALYZING -> CARETAKER_NOTIFIED -> WAITING_FOR_RESPONSE
        language: 'Telugu',
        original_transcript: 'Nenu bathroom lo padipoyanu, levalekapothunnanu.',
        ai_summary: 'Fall / Unable to stand',
        ai_explanation: 'The request indicates a sudden fall and immediate inability to stand up. High risk of injury or hip fracture.',
        created_at: new Date(Date.now() - 36 * 1000).toISOString(),
        assigned_caretaker_id: 201,
        assigned_caretaker_name: 'Ravi Kumar',
        assigned_volunteer_id: null,
        assigned_volunteer_name: null,
        timeline: [
            { time: '13:10', label: 'Voice request captured in Telugu', status: 'done' },
            { time: '13:10', label: 'AI Analyzed: CRITICAL (Priority 94/100)', status: 'done' },
            { time: '13:11', label: 'Primary Caretaker Ravi Kumar notified', status: 'done' },
            { time: '13:11', label: 'Awaiting response (target: 02:00)', status: 'active' }
        ]
    },
    {
        id: 'REQ-1008',
        senior_id: 102,
        senior_name: 'Ramesh',
        senior_age: 68,
        location: 'Home, Vijayawada',
        request_type: 'Medication',
        category: 'Medication',
        urgency: 'WARNING',
        risk_score: 55,
        target_response_seconds: 900,
        seconds_remaining: 420,
        status: 'WAITING_FOR_RESPONSE',
        language: 'Telugu',
        original_transcript: 'Udayam insulin dose marchipoyanu.',
        ai_summary: 'Missed morning medication',
        ai_explanation: 'Senior missed morning diabetic dose. Guidance required to prevent glycemic spike.',
        created_at: new Date(Date.now() - 14 * 60 * 1000).toISOString(),
        assigned_caretaker_id: 201,
        assigned_caretaker_name: 'Ravi Kumar',
        assigned_volunteer_id: null,
        timeline: [
            { time: '08:15', label: 'Medication reminder scheduled', status: 'done' },
            { time: '08:45', label: 'Missed dose flagged', status: 'done' },
            { time: '08:46', label: 'Caretaker notified', status: 'active' }
        ]
    },
    // Past History Requests (Resolved / Expired)
    {
        id: 'REQ-0994',
        senior_id: 101,
        senior_name: 'Lakshmi',
        senior_age: 72,
        location: 'Home, Vijayawada',
        request_type: 'Assistance',
        category: 'Assistance',
        urgency: 'LOW',
        risk_score: 22,
        status: 'RESOLVED',
        language: 'Telugu',
        original_transcript: 'TV remote battery aypoyindi, sahayam kavali.',
        ai_summary: 'Household assistance (TV remote)',
        ai_explanation: 'Non-urgent assistance with household electronic device.',
        created_at: new Date(Date.now() - 26 * 3600 * 1000).toISOString(),
        resolved_at: new Date(Date.now() - 25 * 3600 * 1000).toISOString(),
        assigned_caretaker_id: 201,
        assigned_caretaker_name: 'Ravi Kumar',
        resolution_notes: 'Replaced AAA batteries and verified TV operational.',
        resolution_time_minutes: 45
    },
    {
        id: 'REQ-0980',
        senior_id: 103,
        senior_name: 'Savitri',
        senior_age: 75,
        location: 'Home, Vijayawada',
        request_type: 'Companionship',
        category: 'Companionship',
        urgency: 'LOW',
        risk_score: 15,
        status: 'RESOLVED',
        language: 'Telugu',
        original_transcript: 'Konchem matladadaniki evaraina unte bagunnu.',
        ai_summary: 'Friendly afternoon companionship visit',
        ai_explanation: 'Senior expressed feelings of isolation; requested a friendly check-in.',
        created_at: new Date(Date.now() - 3 * 24 * 3600 * 1000).toISOString(),
        resolved_at: new Date(Date.now() - (3 * 24 * 3600 - 3600) * 1000).toISOString(),
        assigned_caretaker_id: 201,
        assigned_caretaker_name: 'Ravi Kumar',
        resolution_notes: 'Spent 40 minutes over tea, checked blood pressure.',
        resolution_time_minutes: 60
    },
    {
        id: 'REQ-0955',
        senior_id: 101,
        senior_name: 'Lakshmi',
        senior_age: 72,
        location: 'Home, Vijayawada',
        request_type: 'Medical',
        category: 'Medical',
        urgency: 'HIGH',
        risk_score: 82,
        status: 'RESOLVED',
        language: 'English',
        original_transcript: 'Feeling dizzy after taking morning pill.',
        ai_summary: 'Post-medication dizziness',
        ai_explanation: 'Orthostatic symptoms following antihypertensive dose.',
        created_at: new Date(Date.now() - 7 * 24 * 3600 * 1000).toISOString(),
        resolved_at: new Date(Date.now() - (7 * 24 * 3600 - 1800) * 1000).toISOString(),
        assigned_caretaker_id: 201,
        assigned_caretaker_name: 'Ravi Kumar',
        assigned_volunteer_id: 301,
        assigned_volunteer_name: 'Priya Sharma',
        resolution_notes: 'Volunteer Priya arrived in 6 min, monitored pulse and hydration until caretaker arrived.',
        resolution_time_minutes: 30
    }
];

let inMemoryRequests = createInitialRequests();

let inMemoryNotifications = [
    {
        id: 'NOTIF-1',
        type: 'critical',
        title: 'Critical assistance request',
        message: 'Lakshmi reported a fall in the bathroom.',
        timestamp: '13:10 PM',
        read: false,
        requestId: 'REQ-1011'
    },
    {
        id: 'NOTIF-2',
        type: 'warning',
        title: 'Medication reminder pending',
        message: 'Ramesh has not acknowledged morning insulin.',
        timestamp: '08:45 AM',
        read: false,
        requestId: 'REQ-1008'
    },
    {
        id: 'NOTIF-3',
        type: 'info',
        title: 'Daily check-in completed',
        message: 'Savitri completed morning well-being verification.',
        timestamp: '08:00 AM',
        read: true,
        requestId: null
    }
];

export const api = {
    // Authentication
    login: async (role) => {
        await delay(300);
        if (BACKEND_URL) {
            try {
                const res = await fetch(`${BACKEND_URL}/api/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ role })
                });
                if (res.ok) return await res.json();
            } catch (err) {
                console.warn('Backend unavailable, falling back to mock login:', err);
            }
        }
        return mockUsers[role] || mockUsers.senior;
    },

    // Request queries
    getRequests: async (filter = 'all') => {
        await delay(200);
        if (filter === 'all') return [...inMemoryRequests];
        if (filter === 'active') {
            return inMemoryRequests.filter(r => 
                ['CREATED', 'ANALYZING', 'CARETAKER_NOTIFIED', 'WAITING_FOR_RESPONSE', 'ACCEPTED', 'IN_PROGRESS', 'ESCALATED'].includes(r.status)
            );
        }
        if (filter === 'history') {
            return inMemoryRequests.filter(r => 
                ['RESOLVED', 'CANCELLED', 'EXPIRED'].includes(r.status)
            );
        }
        return inMemoryRequests.filter(r => r.category?.toLowerCase() === filter.toLowerCase() || r.status?.toLowerCase() === filter.toLowerCase());
    },

    getActiveRequests: async () => {
        return api.getRequests('active');
    },

    getRequestHistory: async (filter = 'all') => {
        const history = await api.getRequests('history');
        if (filter === 'all') return history;
        return history.filter(r => r.category?.toLowerCase() === filter.toLowerCase() || r.status?.toLowerCase() === filter.toLowerCase());
    },

    // Request creation
    createRequest: async (payload) => {
        await delay(500);
        const newReq = {
            id: `REQ-${Math.floor(1000 + Math.random() * 9000)}`,
            senior_id: payload.senior_id || 101,
            senior_name: payload.senior_name || 'Lakshmi',
            senior_age: payload.senior_age || 72,
            location: payload.location || 'Home, Vijayawada',
            request_type: payload.request_type || 'Assistance',
            category: payload.category || 'General',
            urgency: payload.urgency || 'MEDIUM',
            risk_score: payload.risk_score || 70,
            target_response_seconds: payload.target_response_seconds || 120,
            seconds_remaining: payload.target_response_seconds || 120,
            status: payload.status || 'CARETAKER_NOTIFIED',
            language: payload.language || 'English',
            original_transcript: payload.transcript || '',
            ai_summary: payload.ai_summary || payload.transcript || 'General assistance',
            ai_explanation: payload.ai_explanation || 'AI evaluated the request signals and assigned target priority.',
            created_at: new Date().toISOString(),
            assigned_caretaker_id: 201,
            assigned_caretaker_name: 'Ravi Kumar',
            assigned_volunteer_id: null,
            assigned_volunteer_name: null,
            timeline: [
                { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), label: 'Request captured', status: 'done' },
                { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), label: `AI Analysis: ${payload.urgency || 'MEDIUM'}`, status: 'done' },
                { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), label: 'Primary Caretaker Ravi Kumar notified', status: 'active' }
            ]
        };

        inMemoryRequests = [newReq, ...inMemoryRequests];

        // Add notification
        inMemoryNotifications.unshift({
            id: `NOTIF-${Date.now()}`,
            type: newReq.urgency === 'CRITICAL' ? 'critical' : 'info',
            title: `${newReq.urgency} assistance request: ${newReq.senior_name}`,
            message: newReq.ai_summary,
            timestamp: 'Just now',
            read: false,
            requestId: newReq.id
        });

        return newReq;
    },

    // Accept request
    acceptRequest: async (requestId, caretakerId = 201) => {
        await delay(300);
        inMemoryRequests = inMemoryRequests.map(req => {
            if (req.id === requestId) {
                return {
                    ...req,
                    status: 'ACCEPTED',
                    timeline: [
                        ...req.timeline,
                        { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), label: 'Caretaker accepted request', status: 'done' }
                    ]
                };
            }
            return req;
        });

        inMemoryNotifications.unshift({
            id: `NOTIF-${Date.now()}`,
            type: 'success',
            title: '✓ Caretaker accepted request',
            message: 'Ravi Kumar is attending to the request.',
            timestamp: 'Just now',
            read: false,
            requestId
        });

        return inMemoryRequests.find(r => r.id === requestId);
    },

    // Caretaker timeout / escalate
    escalateRequest: async (requestId) => {
        await delay(300);
        inMemoryRequests = inMemoryRequests.map(req => {
            if (req.id === requestId) {
                return {
                    ...req,
                    status: 'ESCALATED',
                    timeline: [
                        ...req.timeline,
                        { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), label: 'Caretaker response window expired', status: 'warning' },
                        { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), label: 'Escalated to nearby volunteer network', status: 'active' }
                    ]
                };
            }
            return req;
        });

        inMemoryNotifications.unshift({
            id: `NOTIF-${Date.now()}`,
            type: 'warning',
            title: '⚡ Caretaker timeout',
            message: 'Response window expired. Escalated to volunteer network.',
            timestamp: 'Just now',
            read: false,
            requestId
        });

        return inMemoryRequests.find(r => r.id === requestId);
    },

    // Volunteer accepts
    volunteerAcceptRequest: async (requestId, volunteerId = 301) => {
        await delay(300);
        inMemoryRequests = inMemoryRequests.map(req => {
            if (req.id === requestId) {
                return {
                    ...req,
                    status: 'IN_PROGRESS',
                    assigned_volunteer_id: volunteerId,
                    assigned_volunteer_name: 'Priya Sharma',
                    timeline: [
                        ...req.timeline,
                        { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), label: 'Volunteer Priya Sharma accepted (ETA 7 min)', status: 'done' },
                        { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), label: 'Family notified of volunteer dispatch', status: 'done' }
                    ]
                };
            }
            return req;
        });

        inMemoryNotifications.unshift({
            id: `NOTIF-${Date.now()}`,
            type: 'info',
            title: '🧑 Volunteer accepted assistance',
            message: 'Priya Sharma has accepted Lakshmi\'s assistance request.',
            timestamp: 'Just now',
            read: false,
            requestId
        });

        return inMemoryRequests.find(r => r.id === requestId);
    },

    // Resolve request (moves from active to history)
    resolveRequest: async (requestId, notes = 'Assistance provided successfully.') => {
        await delay(300);
        inMemoryRequests = inMemoryRequests.map(req => {
            if (req.id === requestId) {
                return {
                    ...req,
                    status: 'RESOLVED',
                    resolved_at: new Date().toISOString(),
                    resolution_notes: notes,
                    resolution_time_minutes: Math.floor((Date.now() - new Date(req.created_at).getTime()) / 60000) || 5,
                    timeline: [
                        ...req.timeline,
                        { time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), label: `Request resolved: ${notes}`, status: 'done' }
                    ]
                };
            }
            return req;
        });

        inMemoryNotifications.unshift({
            id: `NOTIF-${Date.now()}`,
            type: 'success',
            title: '✓ Request resolved',
            message: `Assistance completed. Moved to history.`,
            timestamp: 'Just now',
            read: false,
            requestId
        });

        return inMemoryRequests.find(r => r.id === requestId);
    },

    // Reject request
    rejectRequest: async (requestId, caretakerId = 201) => {
        return api.escalateRequest(requestId);
    },

    // Senior queries
    getSeniors: async () => {
        await delay(200);
        return [...mockSeniors];
    },

    getSeniorDetails: async (seniorId) => {
        await delay(200);
        const senior = mockSeniors.find(s => s.id === Number(seniorId)) || mockSeniors[0];
        const recentRequests = inMemoryRequests.filter(r => r.senior_id === senior.id);
        return {
            ...senior,
            recent_requests: recentRequests
        };
    },

    // Volunteer queries
    getNearbyVolunteerRequests: async (volunteerId = 301) => {
        await delay(200);
        // Only return requests that require escalation (caretaker timed out / escalated)
        return inMemoryRequests.filter(r => r.status === 'ESCALATED');
    },

    // Notifications
    getNotifications: async () => {
        await delay(150);
        return [...inMemoryNotifications];
    },

    markNotificationRead: async (notifId) => {
        inMemoryNotifications = inMemoryNotifications.map(n => n.id === notifId ? { ...n, read: true } : n);
        return true;
    },

    markAllNotificationsRead: async () => {
        inMemoryNotifications = inMemoryNotifications.map(n => ({ ...n, read: true }));
        return true;
    },

    // Companionship
    sendCompanionshipRequest: async (seniorId = 101, notes = '') => {
        return api.createRequest({
            senior_id: seniorId,
            senior_name: 'Lakshmi',
            request_type: 'Companionship',
            category: 'Companionship',
            urgency: 'LOW',
            risk_score: 20,
            target_response_seconds: 1800,
            transcript: notes || 'I would like some company or a friendly chat.',
            ai_summary: 'Companionship visit requested',
            ai_explanation: 'Social connection request. Care team notified for friendly check-in.'
        });
    },

    // Additional support
    sendAdditionalSupportRequest: async (seniorId, caretakerId, details = {}) => {
        await delay(400);
        inMemoryNotifications.unshift({
            id: `NOTIF-${Date.now()}`,
            type: 'info',
            title: 'Additional support requested',
            message: `Ravi Kumar requested assistance from ${details.caretakerName || 'nearby support'} for senior.`,
            timestamp: 'Just now',
            read: false,
            requestId: null
        });
        return {
            success: true,
            dispatchedTo: details.caretakerName || 'Arun Varma (2.1 km away)'
        };
    },

    // Location Deviation confirmation
    verifyLocationDeviation: async (seniorId, isExpected) => {
        await delay(200);
        return {
            status: isExpected ? 'Expected trip' : 'Unexpected deviation',
            escalate: !isExpected
        };
    },

    // Reset demo state
    resetDemoData: async () => {
        inMemoryRequests = createInitialRequests();
        inMemoryNotifications = [
            {
                id: 'NOTIF-1',
                type: 'critical',
                title: 'Critical assistance request',
                message: 'Lakshmi reported a fall in the bathroom.',
                timestamp: '13:10 PM',
                read: false,
                requestId: 'REQ-1011'
            },
            {
                id: 'NOTIF-2',
                type: 'warning',
                title: 'Medication reminder pending',
                message: 'Ramesh has not acknowledged morning insulin.',
                timestamp: '08:45 AM',
                read: false,
                requestId: 'REQ-1008'
            }
        ];
        return true;
    }
};
