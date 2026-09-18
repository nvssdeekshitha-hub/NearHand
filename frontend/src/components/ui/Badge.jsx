import React from 'react';
import { cn } from '../../utils/cn';

export function Badge({ children, variant = 'gray', className }) {
    const variants = {
        gray: 'bg-slate-100 text-slate-700 border-slate-200',
        success: 'bg-emerald-50 text-emerald-700 border-emerald-200',
        warning: 'bg-amber-50 text-amber-700 border-amber-200',
        emergency: 'bg-rose-50 text-rose-700 border-rose-200',
        critical: 'bg-rose-600 text-white border-rose-600 font-bold',
        primary: 'bg-sky-50 text-sky-700 border-sky-200',
        teal: 'bg-teal-50 text-teal-700 border-teal-200',
    };

    return (
        <span className={cn('inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border', variants[variant], className)}>
            {children}
        </span>
    );
}
