// // import React, { useState } from 'react';
// // import { Link, useNavigate } from 'react-router-dom';
// // import { useAuth } from '../../context/AuthContext';
// // import './Auth.css';

// // const Register = () => {
// //     const navigate = useNavigate();
// //     const { register } = useAuth();
// //     const [step, setStep] = useState(1);
// //     const [formData, setFormData] = useState({
// //         user_type: 'freelancer',
// //         username: '',
// //         email: '',
// //         password: '',
// //         confirm_password: '',
// //         first_name: '',
// //         last_name: '',
// //         accept_terms: false
// //     });
// //     const [loading, setLoading] = useState(false);
// //     const [errors, setErrors] = useState({});

// //     const handleChange = (e) => {
// //         const { name, value, type, checked } = e.target;
// //         setFormData({
// //             ...formData,
// //             [name]: type === 'checkbox' ? checked : value
// //         });
// //         if (errors[name]) setErrors({ ...errors, [name]: null });
// //     };

// //     const handleRoleSelect = (role) => {
// //         setFormData({ ...formData, user_type: role });
// //         setStep(2);
// //     };

// //     const validateForm = () => {
// //         const newErrors = {};
// //         if (!formData.first_name) newErrors.first_name = 'First name is required';
// //         if (!formData.last_name) newErrors.last_name = 'Last name is required';
// //         if (!formData.username) newErrors.username = 'Username is required';
// //         else if (formData.username.length < 3) newErrors.username = 'Username must be at least 3 characters';
// //         if (!formData.email) newErrors.email = 'Email is required';
// //         else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = 'Email is invalid';
// //         if (!formData.password) newErrors.password = 'Password is required';
// //         else if (formData.password.length < 8) newErrors.password = 'Password must be at least 8 characters';
// //         if (formData.password !== formData.confirm_password) {
// //             newErrors.confirm_password = 'Passwords do not match';
// //         }
// //         if (!formData.accept_terms) newErrors.accept_terms = 'You must accept the terms';
// //         setErrors(newErrors);
// //         return Object.keys(newErrors).length === 0;
// //     };

// //     const handleSubmit = async (e) => {
// //         e.preventDefault();
// //         if (!validateForm()) return;
// //         setLoading(true);
// //         try {
// //             const response = await register(formData);
// //             if (response.success) {
// //                 navigate('/dashboard');
// //             }
// //         } catch (error) {
// //             console.error('Registration error:', error);
// //         } finally {
// //             setLoading(false);
// //         }
// //     };

// //     if (step === 1) {
// //         return (
// //             <div className="auth-container">
// //                 <div className="auth-card">
// //                     <div className="auth-header">
// //                         <h2>Join FreelanceHub</h2>
// //                         <p>Choose your account type</p>
// //                     </div>
// //                     <div className="role-cards">
// //                         <div
// //                             className={`role-card ${formData.user_type === 'freelancer' ? 'selected' : ''}`}
// //                             onClick={() => handleRoleSelect('freelancer')}
// //                         >
// //                             <div className="role-icon">💼</div>
// //                             <h3>Freelancer</h3>
// //                             <p>Find work, build your profile, and get hired</p>
// //                         </div>
// //                         <div
// //                             className={`role-card ${formData.user_type === 'recruiter' ? 'selected' : ''}`}
// //                             onClick={() => handleRoleSelect('recruiter')}
// //                         >
// //                             <div className="role-icon">🏢</div>
// //                             <h3>Recruiter</h3>
// //                             <p>Post jobs and find talented freelancers</p>
// //                         </div>
// //                     </div>
// //                     <div className="auth-footer">
// //                         <p>Already have an account? <Link to="/login">Sign in</Link></p>
// //                     </div>
// //                 </div>
// //             </div>
// //         );
// //     }

// //     return (
// //         <div className="auth-container">
// //             <div className="auth-card">
// //                 <button className="back-button" onClick={() => setStep(1)}>
// //                     <i className="fas fa-arrow-left"></i> Back
// //                 </button>
// //                 <div className="auth-header">
// //                     <h2>Create Account</h2>
// //                     <p>Signing up as <span className={`role-badge ${formData.user_type}`}>{formData.user_type}</span></p>
// //                 </div>

// //                 <form onSubmit={handleSubmit} className="auth-form">
// //                     <div className="form-row">
// //                         <div className="form-group">
// //                             <label>First Name</label>
// //                             <input
// //                                 type="text"
// //                                 name="first_name"
// //                                 value={formData.first_name}
// //                                 onChange={handleChange}
// //                                 className={errors.first_name ? 'error' : ''}
// //                                 placeholder="John"
// //                             />
// //                             {errors.first_name && <span className="error-message">{errors.first_name}</span>}
// //                         </div>
// //                         <div className="form-group">
// //                             <label>Last Name</label>
// //                             <input
// //                                 type="text"
// //                                 name="last_name"
// //                                 value={formData.last_name}
// //                                 onChange={handleChange}
// //                                 className={errors.last_name ? 'error' : ''}
// //                                 placeholder="Doe"
// //                             />
// //                             {errors.last_name && <span className="error-message">{errors.last_name}</span>}
// //                         </div>
// //                     </div>

// //                     <div className="form-group">
// //                         <label>Username</label>
// //                         <input
// //                             type="text"
// //                             name="username"
// //                             value={formData.username}
// //                             onChange={handleChange}
// //                             required
// //                             placeholder="johndoe123"
// //                         />
// //                     </div>

// //                     <div className="form-group">
// //                         <label>Email</label>
// //                         <input
// //                             type="email"
// //                             name="email"
// //                             value={formData.email}
// //                             onChange={handleChange}
// //                             className={errors.email ? 'error' : ''}
// //                             placeholder="john@example.com"
// //                         />
// //                         {errors.email && <span className="error-message">{errors.email}</span>}
// //                     </div>

// //                     <div className="form-row">
// //                         <div className="form-group">
// //                             <label>Password</label>
// //                             <input
// //                                 type="password"
// //                                 name="password"
// //                                 value={formData.password}
// //                                 onChange={handleChange}
// //                                 className={errors.password ? 'error' : ''}
// //                                 placeholder="••••••••"
// //                             />
// //                             {errors.password && <span className="error-message">{errors.password}</span>}
// //                         </div>
// //                         <div className="form-group">
// //                             <label>Confirm Password</label>
// //                             <input
// //                                 type="password"
// //                                 name="confirm_password"
// //                                 value={formData.confirm_password}
// //                                 onChange={handleChange}
// //                                 className={errors.confirm_password ? 'error' : ''}
// //                                 placeholder="••••••••"
// //                             />
// //                             {errors.confirm_password && <span className="error-message">{errors.confirm_password}</span>}
// //                         </div>
// //                     </div>

// //                     <div className="form-group checkbox">
// //                         <label className="checkbox-label">
// //                             <input
// //                                 type="checkbox"
// //                                 name="accept_terms"
// //                                 checked={formData.accept_terms}
// //                                 onChange={handleChange}
// //                             />
// //                             <span>I agree to the <Link to="/terms">Terms of Service</Link> and <Link to="/privacy">Privacy Policy</Link></span>
// //                         </label>
// //                         {errors.accept_terms && <span className="error-message">{errors.accept_terms}</span>}
// //                     </div>

// //                     <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
// //                         {loading ? 'Creating Account...' : 'Create Account'}
// //                     </button>
// //                 </form>

// //                 <div className="auth-footer">
// //                     <p>Already have an account? <Link to="/login">Sign in</Link></p>
// //                 </div>
// //             </div>
// //         </div>
// //     );
// // };

// // export default Register;
// import React, { useState } from 'react';
// import { Link, useNavigate } from 'react-router-dom';
// import { useAuth } from '../../context/AuthContext';
// import './Auth.css';

// const Register = () => {
//     const navigate = useNavigate();
//     const { register } = useAuth();
//     const [step, setStep] = useState(1);
//     const [formData, setFormData] = useState({
//         username: '',  // Add this
//         first_name: '',
//         last_name: '',
//         email: '',
//         password: '',
//         confirmPassword: '',
//         role: 'freelancer'
//     });
//     const [loading, setLoading] = useState(false);
//     const [errors, setErrors] = useState({});

//     const handleChange = (e) => {
//         const { name, value, type, checked } = e.target;
//         setFormData({
//             ...formData,
//             [name]: type === 'checkbox' ? checked : value
//         });
//         if (errors[name]) setErrors({ ...errors, [name]: null });
//     };

//     const handleRoleSelect = (role) => {
//         setFormData({ ...formData, user_type: role });
//         setStep(2);
//     };

//     const validateForm = () => {
//         const newErrors = {};
//         if (!formData.first_name) newErrors.first_name = 'First name is required';
//         if (!formData.last_name) newErrors.last_name = 'Last name is required';
//         if (!formData.username) newErrors.username = 'Username is required';
//         else if (formData.username.length < 3) newErrors.username = 'Username must be at least 3 characters';
//         if (!formData.email) newErrors.email = 'Email is required';
//         else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = 'Email is invalid';
//         if (!formData.password) newErrors.password = 'Password is required';
//         else if (formData.password.length < 8) newErrors.password = 'Password must be at least 8 characters';
//         if (formData.password !== formData.confirm_password) {
//             newErrors.confirm_password = 'Passwords do not match';
//         }
//         if (!formData.accept_terms) newErrors.accept_terms = 'You must accept the terms';
//         setErrors(newErrors);
//         return Object.keys(newErrors).length === 0;
//     };

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         if (!validateForm()) return;
//         setLoading(true);
//         try {
//             const response = await register(formData);
//             if (response.success) {
//                 navigate('/dashboard');
//             }
//         } catch (error) {
//             console.error('Registration error:', error);
//         } finally {
//             setLoading(false);
//         }

//     };

//     if (step === 1) {
//         return (
//             <div className="auth-container">
//                 <div className="auth-card">
//                     <div className="auth-header">
//                         <h2>Join FreelanceHub</h2>
//                         <p>Choose your account type</p>
//                     </div>
//                     <div className="role-cards">
//                         <div
//                             className={`role-card ${formData.user_type === 'freelancer' ? 'selected' : ''}`}
//                             onClick={() => handleRoleSelect('freelancer')}
//                         >
//                             <div className="role-icon">💼</div>
//                             <h3>Freelancer</h3>
//                             <p>Find work, build your profile, and get hired</p>
//                         </div>
//                         <div
//                             className={`role-card ${formData.user_type === 'recruiter' ? 'selected' : ''}`}
//                             onClick={() => handleRoleSelect('recruiter')}
//                         >
//                             <div className="role-icon">🏢</div>
//                             <h3>Recruiter</h3>
//                             <p>Post jobs and find talented freelancers</p>
//                         </div>
//                     </div>
//                     <div className="auth-footer">
//                         <p>Already have an account? <Link to="/login">Sign in</Link></p>
//                     </div>
//                 </div>
//             </div>
//         );
//     }

//     return (
//         <div className="auth-container">
//             <div className="auth-card">
//                 <button className="back-button" onClick={() => setStep(1)}>
//                     <i className="fas fa-arrow-left"></i> Back
//                 </button>
//                 <div className="auth-header">
//                     <h2>Create Account</h2>
//                     <p>Signing up as <span className={`role-badge ${formData.user_type}`}>{formData.user_type}</span></p>
//                 </div>

//                 <form onSubmit={handleSubmit} className="auth-form">
//                     <div className="form-row">
//                         <div className="form-group">
//                             <label>First Name</label>
//                             <input
//                                 type="text"
//                                 name="first_name"
//                                 value={formData.first_name}
//                                 onChange={handleChange}
//                                 className={errors.first_name ? 'error' : ''}
//                                 placeholder="John"
//                                 autoComplete="given-name"  // ← ADD THIS
//                             />
//                             {errors.first_name && <span className="error-message">{errors.first_name}</span>}
//                         </div>
//                         <div className="form-group">
//                             <label>Last Name</label>
//                             <input
//                                 type="text"
//                                 name="last_name"
//                                 value={formData.last_name}
//                                 onChange={handleChange}
//                                 className={errors.last_name ? 'error' : ''}
//                                 placeholder="Doe"
//                                 autoComplete="family-name"  // ← ADD THIS
//                             />
//                             {errors.last_name && <span className="error-message">{errors.last_name}</span>}
//                         </div>
//                     </div>

//                     <div className="form-group">
//                         <label>Username</label>
//                         <input
//                             type="text"
//                             name="username"
//                             value={formData.username}
//                             onChange={handleChange}
//                             required
//                             placeholder="johndoe123"
//                             autoComplete="username"  // ← ADD THIS
//                         />
//                     </div>

//                     <div className="form-group">
//                         <label>Email</label>
//                         <input
//                             type="email"
//                             name="email"
//                             value={formData.email}
//                             onChange={handleChange}
//                             className={errors.email ? 'error' : ''}
//                             placeholder="john@example.com"
//                             autoComplete="email"  // ← ADD THIS
//                         />
//                         {errors.email && <span className="error-message">{errors.email}</span>}
//                     </div>

//                     <div className="form-row">
//                         <div className="form-group">
//                             <label>Password</label>
//                             <input
//                                 type="password"
//                                 name="password"
//                                 value={formData.password}
//                                 onChange={handleChange}
//                                 className={errors.password ? 'error' : ''}
//                                 placeholder="••••••••"
//                                 autoComplete="new-password"  // ← ADD THIS
//                             />
//                             {errors.password && <span className="error-message">{errors.password}</span>}
//                         </div>
//                         <div className="form-group">
//                             <label>Confirm Password</label>
//                             <input
//                                 type="password"
//                                 name="confirm_password"
//                                 value={formData.confirm_password}
//                                 onChange={handleChange}
//                                 className={errors.confirm_password ? 'error' : ''}
//                                 placeholder="••••••••"
//                                 autoComplete="new-password"  // ← ADD THIS
//                             />
//                             {errors.confirm_password && <span className="error-message">{errors.confirm_password}</span>}
//                         </div>
//                     </div>

//                     <div className="form-group checkbox">
//                         <label className="checkbox-label">
//                             <input
//                                 type="checkbox"
//                                 name="accept_terms"
//                                 checked={formData.accept_terms}
//                                 onChange={handleChange}
//                                 autoComplete="off"  // ← ADD THIS
//                             />
//                             <span>I agree to the <Link to="/terms">Terms of Service</Link> and <Link to="/privacy">Privacy Policy</Link></span>
//                         </label>
//                         {errors.accept_terms && <span className="error-message">{errors.accept_terms}</span>}
//                     </div>

//                     <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
//                         {loading ? 'Creating Account...' : 'Create Account'}
//                     </button>
//                 </form>

//                 <div className="auth-footer">
//                     <p>Already have an account? <Link to="/login">Sign in</Link></p>
//                 </div>
//             </div>
//         </div>
//     );
// };

// export default Register;
// Register.jsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Auth.css';

const Register = () => {
    const navigate = useNavigate();
    const { register } = useAuth();
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: '',
        user_type: 'freelancer',  // This matches database column name
        accept_terms: false
    });
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});
    const [serverError, setServerError] = useState('');

    // Username availability states
    const [usernameAvailable, setUsernameAvailable] = useState(null);
    const [checkingUsername, setCheckingUsername] = useState(false);
    const [usernameSuggestions, setUsernameSuggestions] = useState([]);
    let usernameTimeout;

    // Password strength states
    const [passwordStrength, setPasswordStrength] = useState({
        score: 0,
        hasLower: false,
        hasUpper: false,
        hasNumber: false,
        hasSpecial: false,
        isLongEnough: false
    });

    // Check username availability
    const checkUsernameAvailability = async (username) => {
        if (username.length < 3) {
            setUsernameAvailable(null);
            setUsernameSuggestions([]);
            return;
        }

        setCheckingUsername(true);
        try {
            const response = await fetch(`/api/auth/check-username?username=${encodeURIComponent(username)}`);
            const data = await response.json();

            if (data.success) {
                setUsernameAvailable(data.available);
                if (!data.available && data.suggestions) {
                    setUsernameSuggestions(data.suggestions);
                } else {
                    setUsernameSuggestions([]);
                }
            }
        } catch (error) {
            console.error('Error checking username:', error);
        } finally {
            setCheckingUsername(false);
        }
    };

    // Handle input changes
    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;

        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));

        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: null }));
        }

        if (serverError) setServerError('');

        if (name === 'username') {
            if (usernameTimeout) clearTimeout(usernameTimeout);
            usernameTimeout = setTimeout(() => {
                checkUsernameAvailability(value);
            }, 500);
        }

        if (name === 'password') {
            checkPasswordStrength(value);
        }
    };

    // Check password strength
    const checkPasswordStrength = (password) => {
        const strength = {
            hasLower: /[a-z]/.test(password),
            hasUpper: /[A-Z]/.test(password),
            hasNumber: /\d/.test(password),
            hasSpecial: /[!@#$%^&*(),.?":{}|<>]/.test(password),
            isLongEnough: password.length >= 8
        };

        let score = 0;
        if (strength.hasLower) score++;
        if (strength.hasUpper) score++;
        if (strength.hasNumber) score++;
        if (strength.hasSpecial) score++;
        if (strength.isLongEnough) score++;

        setPasswordStrength({ ...strength, score });
    };

    // Get password strength text and color
    const getPasswordStrengthInfo = () => {
        const { score } = passwordStrength;
        if (score <= 2) return { text: 'Weak', color: '#dc3545' };
        if (score <= 3) return { text: 'Medium', color: '#ffc107' };
        if (score <= 4) return { text: 'Good', color: '#17a2b8' };
        return { text: 'Strong', color: '#28a745' };
    };

    // Validate form
    const validateForm = () => {
        const newErrors = {};

        if (!formData.first_name?.trim()) {
            newErrors.first_name = 'First name is required';
        } else if (formData.first_name.length < 2) {
            newErrors.first_name = 'First name must be at least 2 characters';
        }

        if (!formData.last_name?.trim()) {
            newErrors.last_name = 'Last name is required';
        } else if (formData.last_name.length < 2) {
            newErrors.last_name = 'Last name must be at least 2 characters';
        }

        if (!formData.username?.trim()) {
            newErrors.username = 'Username is required';
        } else if (formData.username.length < 3) {
            newErrors.username = 'Username must be at least 3 characters';
        } else if (formData.username.length > 30) {
            newErrors.username = 'Username must be less than 30 characters';
        } else if (!/^[a-zA-Z0-9_]+$/.test(formData.username)) {
            newErrors.username = 'Username can only contain letters, numbers, and underscores';
        } else if (usernameAvailable === false) {
            newErrors.username = 'This username is already taken';
        }

        if (!formData.email?.trim()) {
            newErrors.email = 'Email is required';
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
            newErrors.email = 'Please enter a valid email address';
        }

        if (!formData.password) {
            newErrors.password = 'Password is required';
        } else if (formData.password.length < 8) {
            newErrors.password = 'Password must be at least 8 characters';
        } else if (passwordStrength.score < 3) {
            newErrors.password = 'Password is too weak. Include uppercase, lowercase, numbers, and special characters';
        }

        if (!formData.confirm_password) {
            newErrors.confirm_password = 'Please confirm your password';
        } else if (formData.password !== formData.confirm_password) {
            newErrors.confirm_password = 'Passwords do not match';
        }

        if (!formData.accept_terms) {
            newErrors.accept_terms = 'You must accept the terms and conditions';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    // Handle role selection
    const handleRoleSelect = (role) => {
        setFormData(prev => ({ ...prev, user_type: role }));
        setStep(2);
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!validateForm()) return;

        setLoading(true);
        setServerError('');

        try {
            // Create the data object to send - IMPORTANT: Match backend expectations
            const registrationData = {
                username: formData.username,
                first_name: formData.first_name,
                last_name: formData.last_name,
                email: formData.email,
                password: formData.password,
                confirm_password: formData.confirm_password,
                user_type: formData.user_type,  // Using user_type (with underscore) to match database
                accept_terms: formData.accept_terms
            };

            console.log('Sending registration data:', registrationData);

            const response = await register(registrationData);

            if (response && response.success) {
                // Redirect based on user type
                if (formData.user_type === 'recruiter') {
                    navigate('/recruiter/dashboard');
                } else {
                    navigate('/freelancer/dashboard');
                }
            } else {
                setServerError(response?.message || 'Registration failed. Please try again.');
            }
        } catch (error) {
            console.error('Registration error details:', error);

            // Better error handling
            if (error.response) {
                // The request was made and the server responded with a status code
                console.error('Error response data:', error.response.data);
                console.error('Error response status:', error.response.status);
                setServerError(error.response.data?.message || `Server error: ${error.response.status}`);
            } else if (error.request) {
                // The request was made but no response was received
                console.error('No response received:', error.request);
                setServerError('No response from server. Please check if the server is running.');
            } else {
                // Something happened in setting up the request
                setServerError(error.message || 'An unexpected error occurred');
            }

            // If username is taken, check availability again
            if (error.response?.data?.message?.toLowerCase().includes('username') ||
                error.response?.data?.message?.toLowerCase().includes('duplicate')) {
                checkUsernameAvailability(formData.username);
            }
        } finally {
            setLoading(false);
        }
    };

    // Generate username from first and last name
    const generateUsername = () => {
        if (formData.first_name && formData.last_name) {
            const base = `${formData.first_name}${formData.last_name}`.toLowerCase().replace(/[^a-z0-9]/g, '');
            const random = Math.floor(Math.random() * 1000);
            const suggested = `${base}${random}`;

            setFormData(prev => ({ ...prev, username: suggested }));
            checkUsernameAvailability(suggested);
        }
    };

    // Cleanup timeout on unmount
    useEffect(() => {
        return () => {
            if (usernameTimeout) clearTimeout(usernameTimeout);
        };
    }, []);

    // Step 1: Role Selection
    if (step === 1) {
        return (
            <div className="auth-container">
                <div className="auth-card">
                    <div className="auth-header">
                        <h2>Join FreelanceHub</h2>
                        <p>Choose your account type</p>
                    </div>

                    <div className="role-cards">
                        <div
                            className={`role-card ${formData.user_type === 'freelancer' ? 'selected' : ''}`}
                            onClick={() => handleRoleSelect('freelancer')}
                        >
                            <div className="role-icon">💼</div>
                            <h3>Freelancer</h3>
                            <p>Find work, build your profile, and get hired</p>
                        </div>

                        <div
                            className={`role-card ${formData.user_type === 'recruiter' ? 'selected' : ''}`}
                            onClick={() => handleRoleSelect('recruiter')}
                        >
                            <div className="role-icon">🏢</div>
                            <h3>Recruiter</h3>
                            <p>Post jobs and find talented freelancers</p>
                        </div>
                    </div>

                    <div className="auth-footer">
                        <p>Already have an account? <Link to="/login">Sign in</Link></p>
                    </div>
                </div>
            </div>
        );
    }

    // Step 2: Registration Form
    return (
        <div className="auth-container">
            <div className="auth-card">
                <button className="back-button" onClick={() => setStep(1)}>
                    <i className="fas fa-arrow-left"></i> Back
                </button>

                <div className="auth-header">
                    <h2>Create Account</h2>
                    <p>Signing up as <span className={`role-badge ${formData.user_type}`}>
                        {formData.user_type === 'freelancer' ? 'Freelancer' : 'Recruiter'}
                    </span></p>
                </div>

                {serverError && (
                    <div className="alert alert-error">
                        <i className="fas fa-exclamation-circle"></i>
                        {serverError}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="auth-form">
                    {/* Name Fields */}
                    <div className="form-row">
                        <div className="form-group">
                            <label>First Name <span className="required">*</span></label>
                            <input
                                type="text"
                                name="first_name"
                                value={formData.first_name}
                                onChange={handleChange}
                                className={errors.first_name ? 'error' : ''}
                                placeholder="John"
                                autoComplete="given-name"
                                maxLength="50"
                            />
                            {errors.first_name && (
                                <span className="error-message">{errors.first_name}</span>
                            )}
                        </div>

                        <div className="form-group">
                            <label>Last Name <span className="required">*</span></label>
                            <input
                                type="text"
                                name="last_name"
                                value={formData.last_name}
                                onChange={handleChange}
                                className={errors.last_name ? 'error' : ''}
                                placeholder="Doe"
                                autoComplete="family-name"
                                maxLength="50"
                            />
                            {errors.last_name && (
                                <span className="error-message">{errors.last_name}</span>
                            )}
                        </div>
                    </div>

                    {/* Username Field */}
                    <div className="form-group">
                        <label>Username <span className="required">*</span></label>
                        <div className="username-input-wrapper">
                            <input
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                required
                                placeholder="johndoe123"
                                className={errors.username ? 'error' : ''}
                                autoComplete="username"
                                maxLength="30"
                            />

                            {checkingUsername && (
                                <span className="username-checking">
                                    <i className="fas fa-spinner fa-spin"></i> Checking...
                                </span>
                            )}

                            {!checkingUsername && usernameAvailable === true && formData.username.length >= 3 && (
                                <span className="username-available">
                                    <i className="fas fa-check-circle"></i> Available
                                </span>
                            )}

                            {!checkingUsername && usernameAvailable === false && formData.username.length >= 3 && (
                                <span className="username-taken">
                                    <i className="fas fa-times-circle"></i> Taken
                                </span>
                            )}
                        </div>

                        {errors.username && (
                            <span className="error-message">{errors.username}</span>
                        )}

                        {/* Username Suggestions */}
                        {usernameSuggestions.length > 0 && (
                            <div className="username-suggestions">
                                <p>Suggestions:</p>
                                <div className="suggestion-buttons">
                                    {usernameSuggestions.map((suggestion, index) => (
                                        <button
                                            key={index}
                                            type="button"
                                            className="suggestion-btn"
                                            onClick={() => {
                                                setFormData(prev => ({ ...prev, username: suggestion }));
                                                checkUsernameAvailability(suggestion);
                                            }}
                                        >
                                            {suggestion}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Generate Username Button */}
                        {formData.first_name && formData.last_name && (
                            <button
                                type="button"
                                className="generate-username-btn"
                                onClick={generateUsername}
                            >
                                <i className="fas fa-sync-alt"></i> Generate Username
                            </button>
                        )}
                    </div>

                    {/* Email Field */}
                    <div className="form-group">
                        <label>Email <span className="required">*</span></label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            className={errors.email ? 'error' : ''}
                            placeholder="john@example.com"
                            autoComplete="email"
                        />
                        {errors.email && (
                            <span className="error-message">{errors.email}</span>
                        )}
                    </div>

                    {/* Password Fields */}
                    <div className="form-row">
                        <div className="form-group">
                            <label>Password <span className="required">*</span></label>
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                className={errors.password ? 'error' : ''}
                                placeholder="••••••••"
                                autoComplete="new-password"
                            />

                            {/* Password Strength Indicator */}
                            {formData.password && (
                                <div className="password-strength">
                                    <div className="strength-bars">
                                        {[1, 2, 3, 4].map((level) => (
                                            <div
                                                key={level}
                                                className={`strength-bar ${passwordStrength.score >= level ? 'active' : ''}`}
                                                style={{
                                                    backgroundColor: passwordStrength.score >= level
                                                        ? getPasswordStrengthInfo().color
                                                        : '#e0e0e0'
                                                }}
                                            />
                                        ))}
                                    </div>
                                    <span
                                        className="strength-text"
                                        style={{ color: getPasswordStrengthInfo().color }}
                                    >
                                        {getPasswordStrengthInfo().text}
                                    </span>
                                </div>
                            )}

                            {/* Password Requirements */}
                            {formData.password && (
                                <div className="password-requirements">
                                    <p className={passwordStrength.isLongEnough ? 'valid' : 'invalid'}>
                                        <i className={`fas ${passwordStrength.isLongEnough ? 'fa-check-circle' : 'fa-circle'}`}></i>
                                        At least 8 characters
                                    </p>
                                    <p className={passwordStrength.hasLower && passwordStrength.hasUpper ? 'valid' : 'invalid'}>
                                        <i className={`fas ${passwordStrength.hasLower && passwordStrength.hasUpper ? 'fa-check-circle' : 'fa-circle'}`}></i>
                                        Uppercase & lowercase letters
                                    </p>
                                    <p className={passwordStrength.hasNumber ? 'valid' : 'invalid'}>
                                        <i className={`fas ${passwordStrength.hasNumber ? 'fa-check-circle' : 'fa-circle'}`}></i>
                                        At least one number
                                    </p>
                                    <p className={passwordStrength.hasSpecial ? 'valid' : 'invalid'}>
                                        <i className={`fas ${passwordStrength.hasSpecial ? 'fa-check-circle' : 'fa-circle'}`}></i>
                                        At least one special character
                                    </p>
                                </div>
                            )}

                            {errors.password && (
                                <span className="error-message">{errors.password}</span>
                            )}
                        </div>

                        <div className="form-group">
                            <label>Confirm Password <span className="required">*</span></label>
                            <input
                                type="password"
                                name="confirm_password"
                                value={formData.confirm_password}
                                onChange={handleChange}
                                className={errors.confirm_password ? 'error' : ''}
                                placeholder="••••••••"
                                autoComplete="new-password"
                            />
                            {errors.confirm_password && (
                                <span className="error-message">{errors.confirm_password}</span>
                            )}
                        </div>
                    </div>

                    {/* Terms and Conditions */}
                    <div className="form-group checkbox">
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                name="accept_terms"
                                checked={formData.accept_terms}
                                onChange={handleChange}
                            />
                            <span>
                                I agree to the <Link to="/terms" target="_blank">Terms of Service</Link> and{' '}
                                <Link to="/privacy" target="_blank">Privacy Policy</Link>
                            </span>
                        </label>
                        {errors.accept_terms && (
                            <span className="error-message">{errors.accept_terms}</span>
                        )}
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        className="btn btn-primary btn-block"
                        disabled={loading || checkingUsername || usernameAvailable === false}
                    >
                        {loading ? (
                            <>
                                <i className="fas fa-spinner fa-spin"></i>
                                Creating Account...
                            </>
                        ) : (
                            'Create Account'
                        )}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>Already have an account? <Link to="/login">Sign in</Link></p>
                </div>
            </div>
        </div>
    );
};

export default Register;