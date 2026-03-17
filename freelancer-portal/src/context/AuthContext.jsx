// import React, { createContext, useState, useEffect, useContext } from 'react';
// import axios from 'axios';
// import toast from 'react-hot-toast';

// const AuthContext = createContext();

// export const useAuth = () => useContext(AuthContext);

// export const AuthProvider = ({ children }) => {
//     const [user, setUser] = useState(null);
//     const [loading, setLoading] = useState(true);
//     const [isAuthenticated, setIsAuthenticated] = useState(false);

//     const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

//     useEffect(() => {
//         checkAuth();
//     }, []);

//     const checkAuth = async () => {
//         try {
//             const token = localStorage.getItem('access_token');
//             if (token) {
//                 const response = await axios.get(`${API_URL}/auth/me`, {
//                     headers: { Authorization: `Bearer ${token}` }
//                 });
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
//         try {
//             const response = await axios.post(`${API_URL}/auth/login`, credentials);
//             if (response.data.success) {
//                 localStorage.setItem('access_token', response.data.access_token);
//                 localStorage.setItem('refresh_token', response.data.refresh_token);
//                 localStorage.setItem('user', JSON.stringify(response.data.user));
//                 setUser(response.data.user);
//                 setIsAuthenticated(true);
//                 toast.success('Login successful!');
//             }
//             return response.data;
//         } catch (error) {
//             toast.error(error.response?.data?.message || 'Login failed');
//             throw error;
//         }
//     };

//     const register = async (userData) => {
//         try {
//             const response = await axios.post(`${API_URL}/auth/register`, userData);
//             if (response.data.success) {
//                 localStorage.setItem('access_token', response.data.access_token);
//                 localStorage.setItem('refresh_token', response.data.refresh_token);
//                 localStorage.setItem('user', JSON.stringify(response.data.user));
//                 setUser(response.data.user);
//                 setIsAuthenticated(true);
//                 toast.success('Registration successful!');
//             }
//             return response.data;
//         } catch (error) {
//             toast.error(error.response?.data?.message || 'Registration failed');
//             throw error;
//         }
//     };

//     const logout = async () => {
//         try {
//             const token = localStorage.getItem('access_token');
//             if (token) {
//                 await axios.post(`${API_URL}/auth/logout`, {}, {
//                     headers: { Authorization: `Bearer ${token}` }
//                 });
//             }
//         } catch (error) {
//             console.error('Logout error:', error);
//         } finally {
//             localStorage.clear();
//             setUser(null);
//             setIsAuthenticated(false);
//             toast.success('Logged out successfully');
//             window.location.href = '/login';
//         }
//     };

//     const value = {
//         user,
//         loading,
//         isAuthenticated,
//         userRole: user?.user_type,
//         login,
//         register,
//         logout
//     };

//     return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
// };
import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';
import emailService from '../services/emailService';
import toast from 'react-hot-toast';

const AuthContext = createContext();

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [token, setToken] = useState(localStorage.getItem('access_token'));
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

    // Configure axios defaults
    axios.defaults.baseURL = API_URL;

    // Add token to all axios requests
    axios.interceptors.request.use(
        config => {
            const token = localStorage.getItem('access_token');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        },
        error => Promise.reject(error)
    );

    // Handle token refresh
    axios.interceptors.response.use(
        response => response,
        async error => {
            const originalRequest = error.config;

            if (error.response?.status === 401 && !originalRequest._retry) {
                originalRequest._retry = true;

                try {
                    const refreshToken = localStorage.getItem('refresh_token');
                    if (refreshToken) {
                        const response = await axios.post('/auth/refresh', {
                            refresh_token: refreshToken
                        });

                        if (response.data.success) {
                            localStorage.setItem('access_token', response.data.access_token);
                            originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;
                            return axios(originalRequest);
                        }
                    }
                } catch (refreshError) {
                    console.error('Token refresh failed:', refreshError);
                    logout();
                }
            }

            return Promise.reject(error);
        }
    );

    useEffect(() => {
        if (token) {
            fetchUser();
        } else {
            setLoading(false);
        }
    }, [token]);

    const fetchUser = async () => {
        try {
            const response = await axios.get('/auth/me');
            if (response.data.success) {
                setUser(response.data.user);
                setIsAuthenticated(true);

                // Show verification toast if not verified
                if (!response.data.user.is_verified) {
                    toast((t) => (
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '1rem',
                            padding: '0.5rem'
                        }}>
                            <span style={{ fontSize: '1.2rem' }}>📧</span>
                            <div style={{ flex: 1 }}>
                                <strong style={{ color: '#fbbf24', display: 'block' }}>
                                    Email Not Verified
                                </strong>
                                <span style={{ fontSize: '0.9rem', color: '#a0b3d9' }}>
                                    Please verify your email to receive notifications
                                </span>
                            </div>
                            <button
                                onClick={() => {
                                    resendVerification();
                                    toast.dismiss(t.id);
                                }}
                                style={{
                                    background: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
                                    border: 'none',
                                    borderRadius: '20px',
                                    padding: '0.5rem 1rem',
                                    color: 'white',
                                    fontSize: '0.8rem',
                                    fontWeight: '600',
                                    cursor: 'pointer',
                                    transition: 'all 0.3s ease'
                                }}
                                onMouseEnter={(e) => {
                                    e.target.style.transform = 'translateY(-2px)';
                                    e.target.style.boxShadow = '0 5px 15px rgba(245, 158, 11, 0.3)';
                                }}
                                onMouseLeave={(e) => {
                                    e.target.style.transform = 'translateY(0)';
                                    e.target.style.boxShadow = 'none';
                                }}
                            >
                                Resend
                            </button>
                        </div>
                    ), {
                        duration: 10000,
                        position: 'top-center',
                        style: {
                            background: '#1e2530',
                            color: '#f1f5f9',
                            border: '2px solid #f59e0b',
                            borderRadius: '16px',
                            boxShadow: '0 10px 25px -5px rgba(245, 158, 11, 0.3)',
                            maxWidth: '500px'
                        }
                    });
                }
            } else {
                throw new Error('Failed to fetch user');
            }
        } catch (error) {
            console.error('Failed to fetch user:', error);
            // Only logout if token is invalid, not on network errors
            if (error.response?.status === 401) {
                logout();
            }
        } finally {
            setLoading(false);
        }
    };

    const login = async (credentials) => {
        try {
            const response = await axios.post('/auth/login', credentials);

            if (response.data.success) {
                const { access_token, refresh_token, user } = response.data;

                localStorage.setItem('access_token', access_token);
                localStorage.setItem('refresh_token', refresh_token);
                localStorage.setItem('user', JSON.stringify(user));

                setToken(access_token);
                setUser(user);
                setIsAuthenticated(true);

                if (!user.is_verified) {
                    toast.success('Login successful! Please verify your email.', {
                        icon: '📧',
                        duration: 6000,
                        style: {
                            background: '#1e2530',
                            color: '#f1f5f9',
                            border: '2px solid #f59e0b',
                            borderRadius: '12px'
                        }
                    });

                    // Show verification banner after 2 seconds
                    setTimeout(() => {
                        showVerificationBanner();
                    }, 2000);

                } else {
                    toast.success(`Welcome back, ${user.first_name || 'User'}!`, {
                        icon: '👋',
                        duration: 3000,
                        style: {
                            background: '#1e2530',
                            color: '#f1f5f9',
                            border: '2px solid #10b981',
                            borderRadius: '12px'
                        }
                    });
                }
            }
            return response.data;
        } catch (error) {
            const message = error.response?.data?.message || 'Login failed';
            toast.error(message, {
                icon: '❌',
                style: {
                    background: '#1e2530',
                    color: '#f1f5f9',
                    border: '2px solid #ef4444',
                    borderRadius: '12px'
                }
            });
            throw error;
        }
    };

    const register = async (userData) => {
        try {
            const response = await axios.post('/auth/register', userData);

            if (response.data.success) {
                const { access_token, refresh_token, user } = response.data;

                localStorage.setItem('access_token', access_token);
                localStorage.setItem('refresh_token', refresh_token);
                localStorage.setItem('user', JSON.stringify(user));

                setToken(access_token);
                setUser(user);
                setIsAuthenticated(true);

                // Custom toast with HTML content
                toast.custom((t) => (
                    <div style={{
                        background: 'linear-gradient(135deg, #1e2530, #14181f)',
                        border: '2px solid #10b981',
                        borderRadius: '16px',
                        padding: '1.5rem',
                        maxWidth: '400px',
                        boxShadow: '0 20px 40px -10px rgba(0, 0, 0, 0.5)',
                        animation: 'slideIn 0.5s ease'
                    }}>
                        <div style={{ fontSize: '3rem', textAlign: 'center', marginBottom: '1rem' }}>
                            🎉
                        </div>
                        <h3 style={{
                            color: '#f1f5f9',
                            marginBottom: '0.5rem',
                            textAlign: 'center',
                            background: 'linear-gradient(135deg, #818cf8, #34d399)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent'
                        }}>
                            Registration Successful!
                        </h3>
                        <p style={{ color: '#a0b3d9', marginBottom: '1rem', textAlign: 'center' }}>
                            Welcome to FreelanceHub, {user.first_name}!
                        </p>
                        <div style={{
                            background: 'rgba(16, 185, 129, 0.1)',
                            border: '1px solid rgba(16, 185, 129, 0.3)',
                            borderRadius: '12px',
                            padding: '1rem',
                            marginBottom: '1rem'
                        }}>
                            <p style={{ color: '#f1f5f9', fontSize: '0.95rem', marginBottom: '0.5rem' }}>
                                📧 Please verify your email address:
                            </p>
                            <p style={{
                                color: '#34d399',
                                fontWeight: '600',
                                fontSize: '0.9rem',
                                wordBreak: 'break-all'
                            }}>
                                {user.email}
                            </p>
                        </div>
                        <button
                            onClick={() => {
                                resendVerification();
                                toast.dismiss(t.id);
                            }}
                            style={{
                                width: '100%',
                                padding: '0.75rem',
                                background: 'linear-gradient(135deg, #6366f1, #10b981)',
                                border: 'none',
                                borderRadius: '30px',
                                color: 'white',
                                fontWeight: '600',
                                cursor: 'pointer',
                                transition: 'all 0.3s ease',
                                marginBottom: '0.5rem'
                            }}
                            onMouseEnter={(e) => {
                                e.target.style.transform = 'translateY(-2px)';
                                e.target.style.boxShadow = '0 10px 20px -5px rgba(99, 102, 241, 0.3)';
                            }}
                            onMouseLeave={(e) => {
                                e.target.style.transform = 'translateY(0)';
                                e.target.style.boxShadow = 'none';
                            }}
                        >
                            Resend Verification Email
                        </button>
                        <button
                            onClick={() => toast.dismiss(t.id)}
                            style={{
                                width: '100%',
                                padding: '0.5rem',
                                background: 'transparent',
                                border: '1px solid #2a3342',
                                borderRadius: '30px',
                                color: '#a0b3d9',
                                cursor: 'pointer',
                                transition: 'all 0.3s ease'
                            }}
                            onMouseEnter={(e) => {
                                e.target.style.background = '#1e2530';
                                e.target.style.color = '#f1f5f9';
                            }}
                            onMouseLeave={(e) => {
                                e.target.style.background = 'transparent';
                                e.target.style.color = '#a0b3d9';
                            }}
                        >
                            Close
                        </button>
                    </div>
                ), {
                    duration: 15000,
                    position: 'top-center'
                });
            }
            return response.data;
        } catch (error) {
            const message = error.response?.data?.message || 'Registration failed';
            toast.error(message, {
                icon: '❌',
                style: {
                    background: '#1e2530',
                    color: '#f1f5f9',
                    border: '2px solid #ef4444',
                    borderRadius: '12px'
                }
            });
            throw error;
        }
    };

    const logout = async () => {
        try {
            await axios.post('/auth/logout');
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
            setToken(null);
            setUser(null);
            setIsAuthenticated(false);

            toast.success('Logged out successfully', {
                icon: '👋',
                duration: 3000,
                style: {
                    background: '#1e2530',
                    color: '#f1f5f9',
                    border: '2px solid #6366f1',
                    borderRadius: '12px'
                }
            });

            // Redirect to login
            window.location.href = '/login';
        }
    };

    const updateUser = (userData) => {
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData));
    };

    const resendVerification = async () => {
        try {
            const response = await emailService.resendVerificationEmail();
            if (response.success) {
                toast.success('Verification email sent! Please check your inbox.', {
                    icon: '📧',
                    duration: 6000,
                    style: {
                        background: '#1e2530',
                        color: '#f1f5f9',
                        border: '2px solid #10b981',
                        borderRadius: '12px'
                    }
                });
            }
            return response;
        } catch (error) {
            const message = error.response?.data?.message || 'Failed to send verification email';
            toast.error(message, {
                icon: '❌',
                style: {
                    background: '#1e2530',
                    color: '#f1f5f9',
                    border: '2px solid #ef4444',
                    borderRadius: '12px'
                }
            });
            throw error;
        }
    };

    const showVerificationBanner = () => {
        toast.custom((t) => (
            <div style={{
                background: 'linear-gradient(135deg, #1e2530, #14181f)',
                border: '2px solid #f59e0b',
                borderRadius: '16px',
                padding: '1.5rem',
                maxWidth: '450px',
                boxShadow: '0 20px 40px -10px rgba(0, 0, 0, 0.5)',
                animation: 'slideIn 0.5s ease'
            }}>
                <div style={{ fontSize: '2.5rem', textAlign: 'center', marginBottom: '1rem' }}>
                    📧
                </div>
                <h3 style={{
                    color: '#fbbf24',
                    marginBottom: '0.5rem',
                    textAlign: 'center'
                }}>
                    Email Verification Required
                </h3>
                <p style={{ color: '#a0b3d9', marginBottom: '1.5rem', textAlign: 'center' }}>
                    Please verify your email address to:
                </p>
                <ul style={{
                    color: '#a0b3d9',
                    marginBottom: '1.5rem',
                    paddingLeft: '1.5rem',
                    listStyle: 'none'
                }}>
                    <li style={{ marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ color: '#10b981' }}>✓</span> Receive job alerts
                    </li>
                    <li style={{ marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ color: '#10b981' }}>✓</span> Get application updates
                    </li>
                    <li style={{ marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ color: '#10b981' }}>✓</span> Connect with recruiters
                    </li>
                </ul>
                <button
                    onClick={() => {
                        resendVerification();
                        toast.dismiss(t.id);
                    }}
                    style={{
                        width: '100%',
                        padding: '0.75rem',
                        background: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
                        border: 'none',
                        borderRadius: '30px',
                        color: 'white',
                        fontWeight: '600',
                        cursor: 'pointer',
                        transition: 'all 0.3s ease',
                        marginBottom: '0.5rem'
                    }}
                    onMouseEnter={(e) => {
                        e.target.style.transform = 'translateY(-2px)';
                        e.target.style.boxShadow = '0 10px 20px -5px rgba(245, 158, 11, 0.3)';
                    }}
                    onMouseLeave={(e) => {
                        e.target.style.transform = 'translateY(0)';
                        e.target.style.boxShadow = 'none';
                    }}
                >
                    Resend Verification Email
                </button>
                <button
                    onClick={() => toast.dismiss(t.id)}
                    style={{
                        width: '100%',
                        padding: '0.5rem',
                        background: 'transparent',
                        border: '1px solid #2a3342',
                        borderRadius: '30px',
                        color: '#a0b3d9',
                        cursor: 'pointer',
                        transition: 'all 0.3s ease'
                    }}
                    onMouseEnter={(e) => {
                        e.target.style.background = '#1e2530';
                        e.target.style.color = '#f1f5f9';
                    }}
                    onMouseLeave={(e) => {
                        e.target.style.background = 'transparent';
                        e.target.style.color = '#a0b3d9';
                    }}
                >
                    Later
                </button>
            </div>
        ), {
            duration: Infinity,
            position: 'top-center'
        });
    };

    const value = {
        user,
        loading,
        isAuthenticated,
        userRole: user?.user_type,
        login,
        register,
        logout,
        updateUser,
        resendVerification,
        token,
        API_URL
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

// Add global styles for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .verification-badge {
        animation: pulse 2s infinite;
    }
`;
document.head.appendChild(style);