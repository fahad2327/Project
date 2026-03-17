// import React, { useState } from 'react';
// import { Link, useNavigate } from 'react-router-dom';
// import { useAuth } from '../../context/AuthContext';
// import './Auth.css';

// const Login = () => {
//     const navigate = useNavigate();
//     const { login } = useAuth();
//     const [formData, setFormData] = useState({
//         email: '',
//         password: '',
//         remember_me: false
//     });
//     const [loading, setLoading] = useState(false);
//     const [errors, setErrors] = useState({});
//     const [showPassword, setShowPassword] = useState(false);

//     const handleChange = (e) => {
//         const { name, value, type, checked } = e.target;
//         setFormData({
//             ...formData,
//             [name]: type === 'checkbox' ? checked : value
//         });
//         if (errors[name]) {
//             setErrors({ ...errors, [name]: null });
//         }
//     };

//     const validateForm = () => {
//         const newErrors = {};
//         if (!formData.email) newErrors.email = 'Email is required';
//         else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = 'Email is invalid';
//         if (!formData.password) newErrors.password = 'Password is required';
//         setErrors(newErrors);
//         return Object.keys(newErrors).length === 0;
//     };

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         if (!validateForm()) return;
//         setLoading(true);
//         try {
//             const response = await login(formData);
//             if (response.success) {
//                 navigate('/dashboard');
//             }
//         } catch (error) {
//             console.error('Login error:', error);
//         } finally {
//             setLoading(false);
//         }
//     };

//     return (
//         <div className="auth-container">
//             <div className="auth-card">
//                 <div className="auth-header">
//                     <h2>Welcome Back</h2>
//                     <p>Sign in to your account</p>
//                 </div>

//                 <form onSubmit={handleSubmit} className="auth-form">
//                     <div className="form-group">
//                         <label htmlFor="email">Email Address</label>
//                         <div className="input-wrapper">
//                             <i className="fas fa-envelope"></i>git status
//                             <input
//                                 type="email"
//                                 id="email"
//                                 name="email"
//                                 value={formData.email}
//                                 onChange={handleChange}
//                                 className={errors.email ? 'error' : ''}
//                                 placeholder="Enter your email"
//                             />
//                         </div>
//                         {errors.email && <span className="error-message">{errors.email}</span>}
//                     </div>

//                     <div className="form-group">
//                         <label htmlFor="password">Password</label>
//                         <div className="input-wrapper">
//                             <i className="fas fa-lock"></i>
//                             <input
//                                 type={showPassword ? 'text' : 'password'}
//                                 id="password"
//                                 name="password"
//                                 value={formData.password}
//                                 onChange={handleChange}
//                                 className={errors.password ? 'error' : ''}
//                                 placeholder="Enter your password"
//                             />
//                             <button
//                                 type="button"
//                                 className="toggle-password"
//                                 onClick={() => setShowPassword(!showPassword)}
//                             >
//                                 <i className={`fas fa-${showPassword ? 'eye-slash' : 'eye'}`}></i>
//                             </button>
//                         </div>
//                         {errors.password && <span className="error-message">{errors.password}</span>}
//                     </div>

//                     <div className="form-options">
//                         <label className="checkbox-label">
//                             <input
//                                 type="checkbox"
//                                 name="remember_me"
//                                 checked={formData.remember_me}
//                                 onChange={handleChange}
//                             />
//                             <span>Remember me</span>
//                         </label>
//                         <Link to="/forgot-password" className="forgot-password">
//                             Forgot password?
//                         </Link>
//                     </div>

//                     <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
//                         {loading ? 'Signing in...' : 'Sign In'}
//                     </button>
//                 </form>

//                 <div className="auth-footer">
//                     <p>
//                         Don't have an account? <Link to="/register">Sign up</Link>
//                     </p>
//                 </div>
//             </div>
//         </div>
//     );
// };

// export default Login;
// src/components/Auth/Login.jsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Auth.css';

const Login = () => {
    const navigate = useNavigate();
    const { login, isAuthenticated, user } = useAuth();
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        remember_me: false
    });
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});
    const [showPassword, setShowPassword] = useState(false);

    // Redirect if already authenticated
    useEffect(() => {
        if (isAuthenticated && user) {
            console.log('Already authenticated, redirecting based on role:', user);

            const userRole = user.user_type;

            if (userRole === 'freelancer') {
                navigate('/freelancer/dashboard', { replace: true });
            } else if (userRole === 'recruiter') {
                navigate('/recruiter/dashboard', { replace: true });
            } else {
                navigate('/dashboard', { replace: true });
            }
        }
    }, [isAuthenticated, user, navigate]);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData({
            ...formData,
            [name]: type === 'checkbox' ? checked : value
        });
        if (errors[name]) {
            setErrors({ ...errors, [name]: null });
        }
    };

    const validateForm = () => {
        const newErrors = {};
        if (!formData.email) newErrors.email = 'Email is required';
        else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = 'Email is invalid';
        if (!formData.password) newErrors.password = 'Password is required';
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!validateForm()) return;

        setLoading(true);

        try {
            console.log('Attempting login with:', formData.email);
            const response = await login(formData);
            console.log('Login response:', response);

            if (!response.success) {
                setLoading(false);
                // Show error message
                if (response.message) {
                    alert(response.message);
                }
            }
            // If successful, the useEffect will handle redirect
        } catch (error) {
            console.error('Login error:', error);
            alert(error.response?.data?.message || 'Login failed');
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h2>Welcome Back</h2>
                    <p>Sign in to your account</p>
                </div>

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label htmlFor="email">Email Address</label>
                        <div className="input-wrapper">
                            <i className="fas fa-envelope"></i>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                className={errors.email ? 'error' : ''}
                                placeholder="Enter your email"
                                autoComplete="email"
                                disabled={loading}
                            />
                        </div>
                        {errors.email && <span className="error-message">{errors.email}</span>}
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <div className="input-wrapper">
                            <i className="fas fa-lock"></i>
                            <input
                                type={showPassword ? 'text' : 'password'}
                                id="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                className={errors.password ? 'error' : ''}
                                placeholder="Enter your password"
                                autoComplete="current-password"
                                disabled={loading}
                            />
                            <button
                                type="button"
                                className="toggle-password"
                                onClick={() => setShowPassword(!showPassword)}
                            >
                                <i className={`fas fa-${showPassword ? 'eye-slash' : 'eye'}`}></i>
                            </button>
                        </div>
                        {errors.password && <span className="error-message">{errors.password}</span>}
                    </div>

                    <div className="form-options">
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                name="remember_me"
                                checked={formData.remember_me}
                                onChange={handleChange}
                                autoComplete="off"
                                disabled={loading}
                            />
                            <span>Remember me</span>
                        </label>
                        <Link to="/forgot-password" className="forgot-password">
                            Forgot password?
                        </Link>
                    </div>

                    <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
                        {loading ? (
                            <>
                                <span className="spinner"></span>
                                Signing in...
                            </>
                        ) : (
                            'Sign In'
                        )}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>
                        Don't have an account? <Link to="/register">Sign up</Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Login;