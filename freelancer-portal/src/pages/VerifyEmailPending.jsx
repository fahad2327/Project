// src/pages/VerifyEmailPending.jsx
import React, { useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-hot-toast';
import './VerifyEmailPending.css';

const VerifyEmailPending = () => {
    const location = useLocation();
    const { user, resendVerification } = useAuth();
    const [resending, setResending] = useState(false);
    const [countdown, setCountdown] = useState(0);
    const email = location.state?.email || user?.email;

    const handleResendEmail = async () => {
        setResending(true);
        setCountdown(60);

        try {
            const response = await resendVerification();
            if (response.success) {
                toast.success('Verification email resent! Check your inbox.', {
                    icon: '📧',
                    duration: 5000
                });
            }
        } catch (error) {
            toast.error('Failed to resend email');
        } finally {
            // Countdown timer
            const timer = setInterval(() => {
                setCountdown(prev => {
                    if (prev <= 1) {
                        clearInterval(timer);
                        setResending(false);
                        return 0;
                    }
                    return prev - 1;
                });
            }, 1000);
        }
    };

    return (
        <div className="verify-pending-container">
            <div className="verify-card">
                <div className="email-icon">📧</div>

                <h1>Verify Your Email</h1>

                <p className="message">
                    We've sent a verification email to:
                </p>

                <div className="email-highlight">
                    {email || 'your email address'}
                </div>

                <div className="info-box">
                    <h4>📌 Next Steps:</h4>
                    <ol>
                        <li>Check your inbox for the verification email</li>
                        <li>Click the verification link in the email</li>
                        <li>Once verified, you can access all features</li>
                    </ol>
                </div>

                <div className="warning-box">
                    <p>
                        <strong>Didn't receive the email?</strong>
                    </p>
                    <p>Check your spam folder or click below to resend.</p>

                    <button
                        onClick={handleResendEmail}
                        className="btn btn-outline"
                        disabled={resending}
                    >
                        {resending
                            ? `Resend in ${countdown}s`
                            : 'Resend Verification Email'
                        }
                    </button>
                </div>

                <div className="tips">
                    <h4>💡 Quick Tips:</h4>
                    <ul>
                        <li>Add noreply@freelancehub.com to your contacts</li>
                        <li>Check spam/junk folder</li>
                        <li>Wait 2-3 minutes for email delivery</li>
                        <li>Make sure you entered the correct email</li>
                    </ul>
                </div>

                <div className="action-links">
                    <Link to="/" className="btn btn-link">Go to Home</Link>
                    <Link to="/contact" className="btn btn-link">Contact Support</Link>
                </div>
            </div>
        </div>
    );
};

export default VerifyEmailPending;