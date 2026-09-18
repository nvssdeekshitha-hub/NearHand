import React from 'react';
import { ShieldAlert, AlertTriangle, X } from 'lucide-react';
import { Modal } from '../common/Modal';
import { Button } from '../ui/Button';

export function EmergencySOSModal({ isOpen, onClose, onConfirm }) {
    return (
        <Modal isOpen={isOpen} onClose={onClose} maxWidth="max-w-md">
            <div className="text-center">
                <div className="w-20 h-20 bg-rose-50 text-rose-600 rounded-full flex items-center justify-center mx-auto mb-5 border-4 border-rose-100 animate-emergency-pulse">
                    <ShieldAlert className="w-10 h-10" />
                </div>

                <h3 className="text-2xl font-black text-slate-900 tracking-tight mb-2">
                    EMERGENCY ASSISTANCE
                </h3>

                <p className="text-lg font-bold text-rose-700 mb-4">
                    Are you sure you need emergency help?
                </p>

                <p className="text-sm text-slate-600 mb-8 leading-relaxed">
                    This will immediately alert your primary caretaker (Ravi Kumar), your family (Anjali), and activate nearby community emergency responders.
                </p>

                <div className="grid grid-cols-2 gap-3">
                    <Button 
                        variant="secondary" 
                        size="lg" 
                        onClick={onClose}
                        className="rounded-2xl"
                    >
                        Cancel
                    </Button>
                    <Button 
                        variant="emergency" 
                        size="lg" 
                        onClick={() => {
                            onClose();
                            onConfirm();
                        }}
                        className="rounded-2xl"
                    >
                        ACTIVATE SOS
                    </Button>
                </div>
            </div>
        </Modal>
    );
}
