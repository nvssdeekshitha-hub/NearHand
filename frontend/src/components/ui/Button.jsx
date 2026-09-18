import React from 'react';
import { cn } from '../../utils/cn';

export const Button = React.forwardRef(({
    className,
    variant = 'primary',
    size = 'md',
    loading = false,
    disabled,
    children,
    ...props
}, ref) => {

    const variants = {
        primary: 'bg-sky-600 hover:bg-sky-700 text-white shadow-sm border border-transparent active:bg-sky-800',
        secondary: 'bg-white hover:bg-slate-50 text-slate-800 border border-slate-200 shadow-sm active:bg-slate-100',
        emergency: 'bg-rose-600 hover:bg-rose-700 text-white font-bold shadow-md shadow-rose-600/20 active:bg-rose-800',
        outline: 'border-2 border-sky-600 text-sky-600 hover:bg-sky-50 active:bg-sky-100',
        ghost: 'text-slate-700 hover:bg-slate-100 active:bg-slate-200',
        success: 'bg-emerald-600 hover:bg-emerald-700 text-white font-semibold shadow-sm active:bg-emerald-800',
        amber: 'bg-amber-500 hover:bg-amber-600 text-white font-semibold shadow-sm active:bg-amber-700',
    };

    const sizes = {
        sm: 'px-3 py-1.5 text-xs font-semibold rounded-lg',
        md: 'px-4 py-2 text-sm font-medium rounded-xl',
        lg: 'px-6 py-3 text-base font-bold rounded-2xl',
        xl: 'px-8 py-4 text-lg font-extrabold rounded-2xl',
        icon: 'p-2 rounded-xl'
    };

    return (
        <button
            ref={ref}
            disabled={disabled || loading}
            className={cn(
                'inline-flex items-center justify-center transition-all duration-150 outline-none focus-visible:ring-2 focus-visible:ring-sky-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed select-none active:scale-[0.98]',
                variants[variant],
                sizes[size],
                className
            )}
            {...props}
        >
            {loading ? (
                <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>Loading...</span>
                </>
            ) : (
                children
            )}
        </button>
    );
});

Button.displayName = 'Button';
