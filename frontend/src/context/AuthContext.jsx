import React, { createContext, useContext, useState } from 'react';
import { api } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(false);

    const login = async (role) => {
        setLoading(true);
        try {
            const userData = await api.login(role);
            setUser(userData);
            return userData;
        } catch (e) {
            console.error("Login failed", e);
        } finally {
            setLoading(false);
        }
    };

    const logout = () => setUser(null);

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
