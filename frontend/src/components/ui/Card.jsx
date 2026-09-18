import React from 'react';
import { cn } from '../../utils/cn';

export function Card({ className, children, ...props }) {
    return (
        <div className={cn('bg-white rounded-2xl shadow-sm border border-slate-100', className)} {...props}>
            {children}
        </div>
    );
}

export function CardHeader({ className, children, ...props }) {
    return (
        <div className={cn('px-5 py-4 border-b border-slate-100', className)} {...props}>
            {children}
        </div>
    );
}

export function CardBody({ className, children, ...props }) {
    return (
        <div className={cn('p-5', className)} {...props}>
            {children}
        </div>
    );
}

export function CardTitle({ className, children, ...props }) {
    return (
        <h3 className={cn('font-semibold text-lg text-slate-900', className)} {...props}>
            {children}
        </h3>
    );
}
