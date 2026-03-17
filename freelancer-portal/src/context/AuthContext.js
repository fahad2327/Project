// import React, { createContext, useState, useEffect, useContext } from 'react';
// import authService from '../services/authService';
// import api from '../services/api';

// const AuthContext = createContext();

// export const useAuth = () => useContext(AuthContext);

// export const AuthProvider = ({ children }) => {
//     const [user, setUser] = useState(null);
//     const [loading, setLoading] = useState(true);
//     const [isAuthenticated, setIsAuthenticated] = useState(false);

//     useEffect(() => {
//         checkAuth();
//     }, []);

//     const checkAuth = async () => {
//         try {
//             const token = localStorage.getItem('access_token');
//             if (token) {
//                 const response = await api.get('/auth/me');
//                 if (response.data.success) {
//                     setUser(response.data.user);
//                     setIsAuthenticated(true);
//                 }
//             }
//         } catch (error) {
//             console.error('Auth check failed:', error);
//             localStorage.clear();
//         } finally {
//             setLoading(false);
//         }
//     };

//     const login = async (credentials) => {
//         const data = await authService.login(credentials);
//         if (data.success) {
//             setUser(data.user);
//             setIsAuthenticated(true);
//         }
//         return data;
//     };

//     const register = async (userData) => {
//         const data = await authService.register(userData);
//         if (data.success) {
//             setUser(data.user);
//             setIsAuthenticated(true);
//         }
//         return data;
//     };

//     const logout = async () => {
//         await authService.logout();
//         setUser(null);
//         setIsAuthenticated(false);
//     };

//     const value = {
//         user,
//         loading,
//         isAuthenticated,
//         login,
//         register,
//         logout,
//         userRole: user?.user_type,
//     };

//     return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
// };
// context/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from "react";
import authService from "../services/authService";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check localStorage on initial load
        const checkAuth = () => {
            const token = authService.getToken();
            const storedUser = authService.getCurrentUser();

            if (token && storedUser) {
                setUser(storedUser);
                setIsAuthenticated(true);
                console.log('User restored from localStorage:', storedUser);
            }
            setLoading(false);
        };

        checkAuth();
    }, []);

    const login = async (credentials) => {
        try {
            const response = await authService.login(credentials);

            if (response.success) {
                // Get user from response
                const userData = response.user;
                setUser(userData);
                setIsAuthenticated(true);
                console.log('Login successful, user set:', userData);
            }

            return response;
        } catch (error) {
            console.error('Login error in context:', error);
            throw error;
        }
    };

    const register = async (userData) => {
        try {
            const response = await authService.register(userData);

            if (response.success) {
                setUser(response.user);
                setIsAuthenticated(true);
            }

            return response;
        } catch (error) {
            console.error('Register error in context:', error);
            throw error;
        }
    };

    const logout = () => {
        authService.logout();
        setUser(null);
        setIsAuthenticated(false);
    };

    const value = {
        user,
        isAuthenticated,
        loading,
        login,
        register,
        logout,
        userRole: user?.user_type
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};