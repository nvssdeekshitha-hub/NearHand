class MockSocketService {
    constructor() {
        this.listeners = {};
    }

    on(event, callback) {
        if (!this.listeners[event]) this.listeners[event] = [];
        this.listeners[event].push(callback);
        return () => this.off(event, callback); // cleanup returned
    }

    off(event, callback) {
        if (!this.listeners[event]) return;
        this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
    }

    emit(event, data) {
        console.log(`[Socket Emit] ${event}`, data);
        if (this.listeners[event]) {
            this.listeners[event].forEach(cb => cb(data));
        }
    }

    // --- DEMO EMITTERS ---
    triggerAiAnalysisComplete(requestId, analysisData) {
        this.emit('AI_ANALYSIS_COMPLETE', { requestId, data: analysisData });
    }

    triggerCaretakerNotified(requestId) {
        this.emit('CARETAKER_NOTIFIED', { requestId });
    }

    triggerCaretakerTimeout(requestId) {
        this.emit('CARETAKER_TIMEOUT', { requestId });
    }

    triggerVolunteerMatched(requestId, volunteer) {
        this.emit('VOLUNTEER_MATCHED', { requestId, volunteer });
    }

    triggerVolunteerAccepted(requestId, volunteerId) {
        this.emit('VOLUNTEER_ACCEPTED', { requestId, volunteerId });
    }

    triggerFamilyNotified(requestId) {
        this.emit('FAMILY_NOTIFIED', { requestId });
    }

    triggerLocationDeviation(seniorId, data) {
        this.emit('LOCATION_DEVIATION', { seniorId, data });
    }
}

export const socket = new MockSocketService();
