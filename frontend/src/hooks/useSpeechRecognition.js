import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * useSpeechRecognition
 * Reusable hook providing browser Web Speech API transcription
 * with multi-language support, recording duration timer, and fallback.
 */
export function useSpeechRecognition() {
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState('');
    const [interimTranscript, setInterimTranscript] = useState('');
    const [error, setError] = useState(null);
    const [recordingDuration, setRecordingDuration] = useState(0);

    const recognitionRef = useRef(null);
    const timerRef = useRef(null);
    const isSupported = typeof window !== 'undefined' && 
        ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window);

    // Stop and cleanup timer
    const clearTimer = useCallback(() => {
        if (timerRef.current) {
            clearInterval(timerRef.current);
            timerRef.current = null;
        }
    }, []);

    // Stop listening safely
    const stopListening = useCallback(() => {
        if (recognitionRef.current && isListening) {
            try {
                recognitionRef.current.stop();
            } catch (err) {
                console.warn('SpeechRecognition stop error:', err);
            }
        }
        setIsListening(false);
        clearTimer();
    }, [isListening, clearTimer]);

    // Start listening
    const startListening = useCallback((languageCode = 'te-IN') => {
        setError(null);
        setInterimTranscript('');
        setRecordingDuration(0);

        if (!isSupported) {
            setError("Voice input isn't supported in this browser. You can type your request instead.");
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        try {
            const recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = languageCode;

            recognition.onstart = () => {
                setIsListening(true);
                clearTimer();
                timerRef.current = setInterval(() => {
                    setRecordingDuration(prev => prev + 1);
                }, 1000);
            };

            recognition.onresult = (event) => {
                let currentInterim = '';
                let finalTranscriptPart = '';

                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    const res = event.results[i];
                    if (res.isFinal) {
                        finalTranscriptPart += res[0].transcript + ' ';
                    } else {
                        currentInterim += res[0].transcript;
                    }
                }

                if (finalTranscriptPart) {
                    setTranscript(prev => (prev ? prev.trim() + ' ' : '') + finalTranscriptPart.trim());
                }
                setInterimTranscript(currentInterim);
            };

            recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                if (event.error === 'not-allowed') {
                    setError('Microphone access was denied. Please allow microphone permissions in your browser settings.');
                } else if (event.error === 'no-speech') {
                    // harmless, user didn't speak yet
                } else if (event.error === 'network') {
                    setError('Network error during voice recognition. Please check your internet connection.');
                } else {
                    setError(`Voice recognition error: ${event.error}`);
                }
                stopListening();
            };

            recognition.onend = () => {
                setIsListening(false);
                clearTimer();
            };

            recognitionRef.current = recognition;
            recognition.start();
        } catch (err) {
            console.error('Failed to initialize SpeechRecognition:', err);
            setError('Could not start voice recognition. Please try typing instead.');
            setIsListening(false);
            clearTimer();
        }
    }, [isSupported, clearTimer, stopListening]);

    const resetTranscript = useCallback(() => {
        setTranscript('');
        setInterimTranscript('');
        setRecordingDuration(0);
        setError(null);
    }, []);

    useEffect(() => {
        return () => {
            clearTimer();
            if (recognitionRef.current) {
                try {
                    recognitionRef.current.abort();
                } catch {
                    // ignore
                }
            }
        };
    }, [clearTimer]);

    // Format duration into mm:ss
    const formattedDuration = `${String(Math.floor(recordingDuration / 60)).padStart(2, '0')}:${String(recordingDuration % 60).padStart(2, '0')}`;

    return {
        isSupported,
        isListening,
        transcript,
        interimTranscript,
        error,
        recordingDuration,
        formattedDuration,
        startListening,
        stopListening,
        resetTranscript,
        setTranscript,
    };
}
