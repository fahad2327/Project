// import React, { useState } from 'react';
// import { Link, useNavigate } from 'react-router-dom';
// import authService from '../../services/authService';
// import './Auth.css';

// const SignIn = ({ onSignIn }) => {
//     const navigate = useNavigate();
//     const [email, setEmail] = useState('');
//     const [password, setPassword] = useState('');
//     const [error, setError] = useState('');
//     const [loading, setLoading] = useState(false);

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         setError('');
//         setLoading(true);

//         try {
//             const data = await authService.login({ email, password });

//             if (data.success) {
//                 onSignIn(data.user);
//                 navigate('/welcome');
//             } else {
//                 setError(data.message || 'Invalid email or password');
//             }
//         } catch (err) {
//             setError('Failed to connect to server. Please try again.');
//             console.error('Login error:', err);
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

//                 {error && <div className="auth-error">{error}</div>}

//                 <form onSubmit={handleSubmit} className="auth-form">
//                     <div className="form-group">
//                         <label htmlFor="email">Email Address</label>
//                         <div className="input-wrapper">
//                             <i className="fas fa-envelope"></i>
//                             <input
//                                 type="email"
//                                 id="email"
//                                 placeholder="Enter your email"
//                                 value={email}
//                                 onChange={(e) => setEmail(e.target.value)}
//                                 required
//                                 disabled={loading}
//                             />
//                         </div>
//                     </div>

//                     <div className="form-group">
//                         <label htmlFor="password">Password</label>
//                         <div className="input-wrapper">
//                             <i className="fas fa-lock"></i>
//                             <input
//                                 type="password"
//                                 id="password"
//                                 placeholder="Enter your password"
//                                 value={password}
//                                 onChange={(e) => setPassword(e.target.value)}
//                                 required
//                                 disabled={loading}
//                             />
//                         </div>
//                     </div>

//                     <div className="form-options">
//                         <label className="remember-me">
//                             <input type="checkbox" /> Remember me
//                         </label>
//                         <Link to="/forgot-password" className="forgot-password">
//                             Forgot Password?
//                         </Link>
//                     </div>

//                     <button
//                         type="submit"
//                         className="auth-button"
//                         disabled={loading}
//                     >
//                         {loading ? 'Signing in...' : 'Sign In'}
//                     </button>

//                     <div className="auth-footer">
//                         Don't have an account?{' '}
//                         <Link to="/signup" className="auth-link">
//                             Sign Up
//                         </Link>
//                     </div>
//                 </form>
//             </div>
//         </div>
//     );
// };

// export default SignIn;