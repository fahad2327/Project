import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import emailService from '../services/emailService';
import toast from 'react-hot-toast';
import './VerifyEmail.css';

const VerifyEmail = () => {
    const { token } = useParams();
    const navigate = useNavigate();
    const { user, resendVerification } = useAuth();
    const [verifying, setVerifying] = useState(true);
    const [verified, setVerified] = useState(false);
    const [error, setError] = useState('');
    const [resending, setResending] = useState(false);
    const [countdown, setCountdown] = useState(60);

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
        }
        return () => clearTimeout(timer);
    }, [resending, countdown]);

    const verifyEmailToken = async () => {
        try {
            const response = await emailService.verifyEmail(token);
            if (response.success) {
                setVerified(true);
                toast.success('Email verified successfully! 🎉');
                setTimeout(() => {
                    navigate('/dashboard');
                }, 3000);
            } else {
                setError(response.message || 'Verification failed');
                toast.error(response.message || 'Verification failed');
            }
        } catch (error) {
            const message = error.response?.data?.message || 'Verification failed';
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
            if (response.success) {
                toast.success('Verification email sent! Please check your inbox.', {
                    duration: 5000,
                    icon: '📧'
                });
            }
        } catch (error) {
            toast.error(error.response?.data?.message || 'Failed to send verification email');
        } finally {
            setTimeout(() => {
                setResending(false);
                setCountdown(60);
            }, 60000);
        }
    };

    const handleGoToDashboard = () => {
        navigate('/dashboard');
    };

    if (verifying) {
        return (
            <div className="verify-container">
                <div className="verify-card">
                    <div className="loader-spinner"></div>
                    <h2>Verifying your email...</h2>
                    <p>Please wait while we verify your email address.</p>
                    <div className="progress-bar">
                        <div className="progress-fill"></div>
                    </div>
                </div>
            </div>
        );
    }

    if (verified) {
        return (
            <div className="verify-container">
                <div className="verify-card success">
                    <div className="success-icon">✓</div>
                    <h2>Email Verified Successfully!</h2>
                    <p>Your email has been verified. You'll be redirected to your dashboard.</p>
                    <div className="button-group">
                        <button onClick={handleGoToDashboard} className="btn btn-primary">
                            Go to Dashboard Now
                        </button>
                        <Link to="/" className="btn btn-outline">
                            Go to Home
                        </Link>
                    </div>
                </div>
            </div>
        );
    }

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