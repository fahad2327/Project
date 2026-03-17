import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import emailService from '../services/emailService';
import toast from 'react-hot-toast';
import './EmailSettings.css';

const EmailSettings = () => {
    const { user, resendVerification } = useAuth();
    const [loading, setLoading] = useState(false);
    const [resending, setResending] = useState(false);
    const [emailPreferences, setEmailPreferences] = useState({
        jobAlerts: true,
        applicationUpdates: true,
        newsletter: false,
        marketingEmails: false,
        messageNotifications: true
    });

    const [emailHistory, setEmailHistory] = useState([]);
    const [historyLoading, setHistoryLoading] = useState(false);
    const [historyPage, setHistoryPage] = useState(1);
    const [hasMore, setHasMore] = useState(true);

    useEffect(() => {
        loadEmailPreferences();
        loadEmailHistory();
    }, []);

    const loadEmailPreferences = async () => {
        try {
            const response = await emailService.getEmailPreferences();
            if (response.success) {
                setEmailPreferences(response.preferences);
            }
        } catch (error) {
            console.error('Failed to load email preferences:', error);
        }
    };

    const loadEmailHistory = async (page = 1) => {
        setHistoryLoading(true);
        try {
            const response = await emailService.getEmailHistory({ page, limit: 10 });
            if (response.success) {
                if (page === 1) {
                    setEmailHistory(response.history);
                } else {
                    setEmailHistory(prev => [...prev, ...response.history]);
                }
                setHasMore(response.hasMore);
                setHistoryPage(page);
            }
        } catch (error) {
            console.error('Failed to load email history:', error);
        } finally {
            setHistoryLoading(false);
        }
    };

    const handlePreferenceChange = (e) => {
        const { name, checked } = e.target;
        setEmailPreferences(prev => ({
            ...prev,
            [name]: checked
        }));
    };

    const savePreferences = async () => {
        setLoading(true);
        try {
            const response = await emailService.updateEmailPreferences(emailPreferences);
            if (response.success) {
                toast.success('Email preferences saved successfully!', {
                    icon: '✅',
                    duration: 3000
                });
            }
        } catch (error) {
            toast.error('Failed to save email preferences');
        } finally {
            setLoading(false);
        }
    };

    const handleResendVerification = async () => {
        setResending(true);
        try {
            const response = await resendVerification();
            if (response.success) {
                toast.success('Verification email sent! Please check your inbox.', {
                    icon: '📧',
                    duration: 5000
                });
            }
        } catch (error) {
            toast.error(error.response?.data?.message || 'Failed to send verification email');
        } finally {
            setResending(false);
        }
    };

    const loadMoreHistory = () => {
        if (hasMore && !historyLoading) {
            loadEmailHistory(historyPage + 1);
        }
    };

    const getStatusIcon = (status) => {
        switch (status) {
            case 'sent': return '✓';
            case 'delivered': return '✓✓';
            case 'opened': return '👁️';
            case 'clicked': return '🖱️';
            case 'failed': return '✗';
            default: return '📧';
        }
    };

    return (
        <div className="email-settings">
            <div className="settings-header">
                <h2>Email Settings</h2>
                <p>Manage your email preferences and notifications</p>
            </div>

            {!user?.is_verified && (
                <div className="verification-banner">
                    <div className="banner-content">
                        <i className="fas fa-exclamation-circle"></i>
                        <div className="banner-text">
                            <strong>Email not verified</strong>
                            <span>Please verify your email to receive important notifications.</span>
                        </div>
                    </div>
                    <button
                        onClick={handleResendVerification}
                        className="btn-verify"
                        disabled={resending}
                    >
                        {resending ? 'Sending...' : 'Resend Verification'}
                    </button>
                </div>
            )}

            <div className="settings-grid">
                <div className="preferences-card">
                    <h3>Email Notifications</h3>
                    <p className="card-subtitle">Choose what emails you want to receive</p>

                    <div className="preferences-list">
                        <label className="preference-item">
                            <input
                                type="checkbox"
                                name="jobAlerts"
                                checked={emailPreferences.jobAlerts}
                                onChange={handlePreferenceChange}
                            />
                            <div className="preference-info">
                                <span className="preference-title">Job Alerts</span>
                                <span className="preference-description">
                                    Receive emails about new jobs matching your skills
                                </span>
                            </div>
                        </label>

                        <label className="preference-item">
                            <input
                                type="checkbox"
                                name="applicationUpdates"
                                checked={emailPreferences.applicationUpdates}
                                onChange={handlePreferenceChange}
                            />
                            <div className="preference-info">
                                <span className="preference-title">Application Updates</span>
                                <span className="preference-description">
                                    Get notified when your application status changes
                                </span>
                            </div>
                        </label>

                        <label className="preference-item">
                            <input
                                type="checkbox"
                                name="messageNotifications"
                                checked={emailPreferences.messageNotifications}
                                onChange={handlePreferenceChange}
                            />
                            <div className="preference-info">
                                <span className="preference-title">Message Notifications</span>
                                <span className="preference-description">
                                    Receive email notifications for new messages
                                </span>
                            </div>
                        </label>

                        <label className="preference-item">
                            <input
                                type="checkbox"
                                name="newsletter"
                                checked={emailPreferences.newsletter}
                                onChange={handlePreferenceChange}
                            />
                            <div className="preference-info">
                                <span className="preference-title">Newsletter</span>
                                <span className="preference-description">
                                    Receive weekly updates and tips
                                </span>
                            </div>
                        </label>

                        <label className="preference-item">
                            <input
                                type="checkbox"
                                name="marketingEmails"
                                checked={emailPreferences.marketingEmails}
                                onChange={handlePreferenceChange}
                            />
                            <div className="preference-info">
                                <span className="preference-title">Marketing Emails</span>
                                <span className="preference-description">
                                    Receive promotional offers and updates
                                </span>
                            </div>
                        </label>
                    </div>

                    <button
                        onClick={savePreferences}
                        className="btn-save"
                        disabled={loading}
                    >
                        {loading ? (
                            <>
                                <span className="spinner-small"></span>
                                Saving...
                            </>
                        ) : (
                            'Save Preferences'
                        )}
                    </button>
                </div>

                <div className="email-stats-card">
                    <h3>Email Statistics</h3>
                    <div className="stats-grid">
                        <div className="stat-item">
                            <span className="stat-value">24</span>
                            <span className="stat-label">Emails Sent</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-value">18</span>
                            <span className="stat-label">Opened</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-value">75%</span>
                            <span className="stat-label">Open Rate</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="email-history">
                <div className="history-header">
                    <h3>Recent Email History</h3>
                    <select className="history-filter" onChange={(e) => loadEmailHistory(1, e.target.value)}>
                        <option value="all">All Types</option>
                        <option value="verification">Verification</option>
                        <option value="application">Applications</option>
                        <option value="job">Job Alerts</option>
                    </select>
                </div>

                <div className="history-list">
                    {emailHistory.length > 0 ? (
                        emailHistory.map((email, index) => (
                            <div key={email.id || index} className="history-item">
                                <div className="history-icon">
                                    {getStatusIcon(email.status)}
                                </div>
                                <div className="history-content">
                                    <div className="history-title-row">
                                        <span className="history-title">{email.subject}</span>
                                        <span className={`history-status ${email.status}`}>
                                            {email.status}
                                        </span>
                                    </div>
                                    <div className="history-meta">
                                        <span className="history-type">{email.type}</span>
                                        <span className="history-date">
                                            {new Date(email.sent_at).toLocaleString()}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className="no-history">
                            <p>No email history yet</p>
                        </div>
                    )}

                    {hasMore && (
                        <button
                            onClick={loadMoreHistory}
                            className="btn-load-more"
                            disabled={historyLoading}
                        >
                            {historyLoading ? 'Loading...' : 'Load More'}
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default EmailSettings;