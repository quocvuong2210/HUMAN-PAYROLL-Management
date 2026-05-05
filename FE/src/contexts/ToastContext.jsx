import React, { createContext, useContext, useState, useCallback } from 'react';
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-react';

const ToastContext = createContext();

export const useToast = () => {
    const context = useContext(ToastContext);
    if (!context) {
        throw new Error('useToast must be used within ToastProvider');
    }
    return context;
};

export const ToastProvider = ({ children }) => {
    const [toasts, setToasts] = useState([]);

    const showToast = useCallback((message, type = 'success', duration = 3000) => {
        const id = Date.now() + Math.random();

        setToasts(prev => [...prev, { id, message, type, duration }]);

        // Auto remove after duration
        if (duration > 0) {
            setTimeout(() => {
                setToasts(prev => prev.filter(toast => toast.id !== id));
            }, duration);
        }
    }, []);

    const removeToast = useCallback((id) => {
        setToasts(prev => prev.filter(toast => toast.id !== id));
    }, []);

    return (
        <ToastContext.Provider value={{ showToast }}>
            {children}
            <ToastContainer toasts={toasts} removeToast={removeToast} />
        </ToastContext.Provider>
    );
};

const ToastContainer = ({ toasts, removeToast }) => {
    return (
        <div className="fixed top-6 right-6 z-[9999] flex flex-col gap-3 pointer-events-none">
            {toasts.map(toast => (
                <Toast key={toast.id} toast={toast} onClose={() => removeToast(toast.id)} />
            ))}
        </div>
    );
};

const Toast = ({ toast, onClose }) => {
    const { message, type } = toast;

    const styles = {
        success: {
            bg: 'bg-emerald-500',
            icon: <CheckCircle2 size={20} />,
            text: 'text-white'
        },
        error: {
            bg: 'bg-red-500',
            icon: <AlertCircle size={20} />,
            text: 'text-white'
        },
        info: {
            bg: 'bg-blue-500',
            icon: <Info size={20} />,
            text: 'text-white'
        },
        warning: {
            bg: 'bg-amber-500',
            icon: <AlertCircle size={20} />,
            text: 'text-white'
        }
    };

    const style = styles[type] || styles.info;

    return (
        <div
            className={`${style.bg} ${style.text} px-6 py-4 rounded-xl shadow-2xl flex items-center gap-3 min-w-[320px] max-w-md pointer-events-auto animate-in slide-in-from-right-5 fade-in duration-300`}
        >
            <div className="flex-shrink-0">
                {style.icon}
            </div>
            <div className="flex-1 text-sm font-semibold">
                {message}
            </div>
            <button
                onClick={onClose}
                className="flex-shrink-0 hover:bg-white/20 rounded-lg p-1 transition-colors"
            >
                <X size={18} />
            </button>
        </div>
    );
};
