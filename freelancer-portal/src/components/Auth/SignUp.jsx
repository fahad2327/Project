// import React, { useState } from 'react';
// import { Link, useNavigate } from 'react-router-dom';
// import authService from '../../services/authService';
// import './Auth.css';

// const SignUp = ({ onSignUp }) => {
//     const navigate = useNavigate();
//     const [name, setName] = useState('');
//     const [email, setEmail] = useState('');
//     const [password, setPassword] = useState('');
//     const [confirmPassword, setConfirmPassword] = useState('');
//     const [error, setError] = useState('');
//     const [loading, setLoading] = useState(false);

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         setError('');

//         if (password !== confirmPassword) {
//             return setError('Passwords do not match');
//         }

//         setLoading(true);

//         try {
//             const data = await authService.register({
//                 name,
//                 email,
//                 password
//             });

//             if (data.success) {
//                 onSignUp(data.user);
//                 navigate('/welcome');
//             } else {
//                 setError(data.message || 'Registration failed');
//             }
//         } catch (err) {
//             setError('Failed to connect to server. Please try again.');
//             console.error('Registration error:', err);
//         } finally {
//             setLoading(false);
//         }
//     };

//     return (
//         <div className="auth-container">
//             <div className="auth-card">
//                 <div className="auth-header">
//                     <h2>Create Account</h2>
//                     <p>Join our freelancer community</p>
//                 </div>

//                 {error && <div className="auth-error">{error}</div>}

//                 <form onSubmit={handleSubmit} className="auth-form">
//                     <div className="form-group">
//                         <label htmlFor="name">Full Name</label>
//                         <div className="input-wrapper">
//                             <i className="fas fa-user"></i>
//                             <input
//                                 type="text"
//                                 id="name"
//                                 placeholder="Enter your full name"
//                                 value={name}
//                                 onChange={(e) => setName(e.target.value)}
//                                 required
//                                 disabled={loading}
//                             />
//                         </div>
//                     </div>

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
//                                 placeholder="Create a password"
//                                 value={password}
//                                 onChange={(e) => setPassword(e.target.value)}
//                                 required
//                                 disabled={loading}
//                             />
//                         </div>
//                         <small className="password-hint">
//                             Must be at least 8 characters with uppercase, lowercase, number & special character
//                         </small>
//                     </div>

//                     <div className="form-group">
//                         <label htmlFor="confirm-password">Confirm Password</label>
//                         <div className="input-wrapper">
//                             <i className="fas fa-lock"></i>
//                             <input
//                                 type="password"
//                                 id="confirm-password"
//                                 placeholder="Confirm your password"
//                                 value={confirmPassword}
//                                 onChange={(e) => setConfirmPassword(e.target.value)}
//                                 required
//                                 disabled={loading}
//                             />
//                         </div>
//                     </div>

//                     <button
//                         type="submit"
//                         className="auth-button"
//                         disabled={loading}
//                     >
//                         {loading ? 'Creating Account...' : 'Sign Up'}
//                     </button>

//                     <div className="auth-footer">
//                         Already have an account?{' '}
//                         <Link to="/signin" className="auth-link">
//                             Sign In
//                         </Link>
//                     </div>
//                 </form>
//             </div>
//         </div>
//     );
// };

// export default SignUp;