// components/VerifyEmail.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import emailService from '../services/emailService';
import toast from 'react-hot-toast';

const VerifyEmail = () => {
    const { token } = useParams();
    const navigate = useNavigate();
    const { user, resendVerification, refreshUser } = useAuth();
    const [verifying, setVerifying] = useState(true);
    const [verified, setVerified] = useState(false);
    const [error, setError] = useState('');
    const [resending, setResending] = useState(false);
    const [countdown, setCountdown] = useState(0);

    useEffect(() => {
        if (token) {
            verifyEmailToken();
        } else {
            setVerifying(false);
        }
    }, [token]);

    useEffect(() => {
        let timer;
        if (resending && countdown > 0) {
            timer = setTimeout(() => setCountdown(countdown - 1), 1000);
        } else if (countdown === 0 && resending) {
            setResending(false);
        }
        return () => clearTimeout(timer);
    }, [resending, countdown]);

    const verifyEmailToken = async () => {
        setVerifying(true);
        try {
            const response = await emailService.verifyEmail(token);

            if (response.success) {
                setVerified(true);
                toast.success('Email verified successfully! 🎉');

                // Refresh user data
                if (refreshUser) {
                    await refreshUser();
                }

                // Redirect after 3 seconds
                setTimeout(() => {
                    navigate('/dashboard');
                }, 3000);
            } else {
                setError(response.message || 'Verification failed');
                toast.error(response.message || 'Verification failed');
            }
        } catch (error) {
            const message = error.response?.data?.message ||
                error.message ||
                'Verification failed. Please try again.';
            setError(message);
            toast.error(message);
        } finally {
            setVerifying(false);
        }
    };

    const handleResendVerification = async () => {
        setResending(true);
        setCountdown(60);

        try {
            const response = await resendVerification();
            if (response?.success) {
                toast.success('Verification email sent! Please check your inbox.', {
                    duration: 5000,
                    icon: '📧'
                });
            } else {
                toast.error(response?.message || 'Failed to send verification email');
                setResending(false);
            }
        } catch (error) {
            toast.error(error.response?.data?.message || 'Failed to send verification email');
            setResending(false);
        }
    };

    const handleGoToDashboard = () => {
        navigate('/dashboard');
    };

    // Loading state
    if (verifying) {
        return (
            <div className="verify-container">
                <div className="verify-card">
                    <div className="loader-spinner"></div>
                    <h2>Verifying your email...</h2>
                    <p>Please wait while we verify your email address.</p>
                </div>
            </div>
        );
    }

    // Success state
    if (verified) {
        return (
            <div className="verify-container">
                <div className="verify-card success">
                    <div className="success-icon">✓</div>
                    <h2>Email Verified Successfully!</h2>
                    <p>Your email has been verified. Redirecting to dashboard...</p>
                    <button onClick={handleGoToDashboard} className="btn btn-primary">
                        Go to Dashboard Now
                    </button>
                </div>
            </div>
        );
    }

    // Error state
    if (error) {
        return (
            <div className="verify-container">
                <div className="verify-card error">
                    <div className="error-icon">!</div>
                    <h2>Verification Failed</h2>
                    <p className="error-message">{error}</p>

                    {user && !user.is_verified && (
                        <div className="resend-section">
                            <p>Need a new verification link?</p>
                            <button
                                onClick={handleResendVerification}
                                className="btn btn-primary"
                                disabled={resending}
                            >
                                {resending ? `Resend in ${countdown}s` : 'Resend Verification Email'}
                            </button>
                        </div>
                    )}

                    <div className="button-group">
                        <Link to="/contact" className="btn btn-outline">
                            Contact Support
                        </Link>
                        <Link to="/" className="btn btn-outline">
                            Go to Home
                        </Link>
                    </div>
                </div>
            </div>
        );
    }

    // Default state (no token, just prompt to verify)
    return (
        <div className="verify-container">
            <div className="verify-card">
                <div className="email-icon">📧</div>
                <h2>Verify Your Email</h2>
                <p>We've sent a verification email to:</p>
                <p className="user-email">{user?.email || 'your email'}</p>
                <p className="instruction">Please check your inbox and click the verification link.</p>

                <div className="resend-section">
                    <p>Didn't receive the email?</p>
                    <button
                        onClick={handleResendVerification}
                        className="btn btn-outline"
                        disabled={resending}
                    >
                        {resending ? `Resend in ${countdown}s` : 'Resend Verification Email'}
                    </button>
                </div>

                <div className="tips">
                    <h4>Quick Tips:</h4>
                    <ul>
                        <li>Check your spam/junk folder</li>
                        <li>Add noreply@freelancehub.com to your contacts</li>
                        <li>Wait a few minutes for the email to arrive</li>
                    </ul>
                </div>

                <Link to="/" className="btn btn-link">
                    Return to Home
                </Link>
            </div>
        </div>
    );
};

export default VerifyEmail;