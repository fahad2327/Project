import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Auth.css';

const Register = () => {
    const navigate = useNavigate();
    const { register } = useAuth();
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        user_type: 'freelancer',
        username: '',
        email: '',
        password: '',
        confirm_password: '',
        first_name: '',
        last_name: '',
        accept_terms: false
    });
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData({
            ...formData,
            [name]: type === 'checkbox' ? checked : value
        });
        if (errors[name]) setErrors({ ...errors, [name]: null });
    };

    const handleRoleSelect = (role) => {
        setFormData({ ...formData, user_type: role });
        setStep(2);
    };

    const validateForm = () => {
        const newErrors = {};
        if (!formData.first_name) newErrors.first_name = 'First name is required';
        if (!formData.last_name) newErrors.last_name = 'Last name is required';
        if (!formData.username) newErrors.username = 'Username is required';
        else if (formData.username.length < 3) newErrors.username = 'Username must be at least 3 characters';
        if (!formData.email) newErrors.email = 'Email is required';
        else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = 'Email is invalid';
        if (!formData.password) newErrors.password = 'Password is required';
        else if (formData.password.length < 8) newErrors.password = 'Password must be at least 8 characters';
        if (formData.password !== formData.confirm_password) {
            newErrors.confirm_password = 'Passwords do not match';
        }
        if (!formData.accept_terms) newErrors.accept_terms = 'You must accept the terms';
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!validateForm()) return;
        setLoading(true);
        try {
            const response = await register(formData);
            if (response.success) {
                navigate('/dashboard');
            }
        } catch (error) {
            console.error('Registration error:', error);
        } finally {
            setLoading(false);
        }
    };

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

    return (
        <div className="auth-container">
            <div className="auth-card">
                <button className="back-button" onClick={() => setStep(1)}>
                    <i className="fas fa-arrow-left"></i> Back
                </button>
                <div className="auth-header">
                    <h2>Create Account</h2>
                    <p>Signing up as <span className={`role-badge ${formData.user_type}`}>{formData.user_type}</span></p>
                </div>

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-row">
                        <div className="form-group">
                            <label>First Name</label>
                            <input
                                type="text"
                                name="first_name"
                                value={formData.first_name}
                                onChange={handleChange}
                                className={errors.first_name ? 'error' : ''}
                                placeholder="John"
                            />
                            {errors.first_name && <span className="error-message">{errors.first_name}</span>}
                        </div>
                        <div className="form-group">
                            <label>Last Name</label>
                            <input
                                type="text"
                                name="last_name"
                                value={formData.last_name}
                                onChange={handleChange}
                                className={errors.last_name ? 'error' : ''}
                                placeholder="Doe"
                            />
                            {errors.last_name && <span className="error-message">{errors.last_name}</span>}
                        </div>
                    </div>

                  // In your form, ensure username field is present:
                    <div className="form-group">
                        <label>Username</label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            required
                            placeholder="johndoe123"
                        />
                    </div>

                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            className={errors.email ? 'error' : ''}
                            placeholder="john@example.com"
                        />
                        {errors.email && <span className="error-message">{errors.email}</span>}
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Password</label>
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                className={errors.password ? 'error' : ''}
                                placeholder="••••••••"
                            />
                            {errors.password && <span className="error-message">{errors.password}</span>}
                        </div>
                        <div className="form-group">
                            <label>Confirm Password</label>
                            <input
                                type="password"
                                name="confirm_password"
                                value={formData.confirm_password}
                                onChange={handleChange}
                                className={errors.confirm_password ? 'error' : ''}
                                placeholder="••••••••"
                            />
                            {errors.confirm_password && <span className="error-message">{errors.confirm_password}</span>}
                        </div>
                    </div>

                    <div className="form-group checkbox">
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                name="accept_terms"
                                checked={formData.accept_terms}
                                onChange={handleChange}
                            />
                            <span>I agree to the <Link to="/terms">Terms of Service</Link> and <Link to="/privacy">Privacy Policy</Link></span>
                        </label>
                        {errors.accept_terms && <span className="error-message">{errors.accept_terms}</span>}
                    </div>

                    <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
                        {loading ? 'Creating Account...' : 'Create Account'}
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