import React, { createContext, useState, useEffect, useContext } from 'react';
import authService from '../services/authService';
import api from '../services/api';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        try {
            const token = localStorage.getItem('access_token');
            if (token) {
                const response = await api.get('/auth/me');
                if (response.data.success) {
                    setUser(response.data.user);
                    setIsAuthenticated(true);
                }
            }
        } catch (error) {
            console.error('Auth check failed:', error);
            localStorage.clear();
        } finally {
            setLoading(false);
        }
    };

    const login = async (credentials) => {
        const data = await authService.login(credentials);
        if (data.success) {
            setUser(data.user);
            setIsAuthenticated(true);
        }
        return data;
    };

    const register = async (userData) => {
        const data = await authService.register(userData);
        if (data.success) {
            setUser(data.user);
            setIsAuthenticated(true);
        }
        return data;
    };

    const logout = async () => {
        await authService.logout();
        setUser(null);
        setIsAuthenticated(false);
    };

    const value = {
        user,
        loading,
        isAuthenticated,
        login,
        register,
        logout,
        userRole: user?.user_type,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};