import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import recruiterService from '../../services/recruiterService';
import notificationService from '../../services/notificationService';
import Loader from '../common/Loader';
import './Recruiter.css';

const RecruiterDashboard = () => {
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        fetchDashboardData();
        fetchNotifications();
    }, []);

    const fetchDashboardData = async () => {
        try {
            const response = await recruiterService.getDashboard();
            if (response.success) {
                setDashboardData(response);
            }
        } catch (error) {
            console.error('Failed to fetch dashboard data:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchNotifications = async () => {
        try {
            const response = await notificationService.getNotifications({ limit: 5 });
            setNotifications(response.notifications);
        } catch (error) {
            console.error('Failed to fetch notifications:', error);
        }
    };

    if (loading) return <Loader />;

    const { profile, stats, recent_jobs, recent_applications } = dashboardData || {};

    return (
        <div className="recruiter-dashboard">
            {/* Welcome Section */}
            <div className="welcome-section">
                <div className="welcome-content">
                    <h1>
                        Welcome back, {profile?.company_name}! 👋
                    </h1>
                    <p>Here's what's happening with your job postings today.</p>
                </div>
                <Link to="/post-job" className="btn btn-primary btn-large">
                    <i className="fas fa-plus-circle"></i>
                    Post New Job
                </Link>
            </div>

            {/* Stats Grid */}
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-icon">
                        <i className="fas fa-briefcase"></i>
                    </div>
                    <div className="stat-details">
                        <h3>{stats?.total_jobs || 0}</h3>
                        <p>Total Jobs</p>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon active">
                        <i className="fas fa-check-circle"></i>
                    </div>
                    <div className="stat-details">
                        <h3>{stats?.active_jobs || 0}</h3>
                        <p>Active Jobs</p>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon applications">
                        <i className="fas fa-users"></i>
                    </div>
                    <div className="stat-details">
                        <h3>{stats?.total_applications || 0}</h3>
                        <p>Total Applications</p>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon pending">
                        <i className="fas fa-clock"></i>
                    </div>
                    <div className="stat-details">
                        <h3>{stats?.pending_applications || 0}</h3>
                        <p>Pending Review</p>
                    </div>
                </div>
            </div>

            {/* Main Content Grid */}
            <div className="dashboard-grid">
                {/* Recent Jobs */}
                <div className="dashboard-card recent-jobs">
                    <div className="card-header">
                        <h3>
                            <i className="fas fa-briefcase"></i>
                            Your Active Jobs
                        </h3>
                        <Link to="/manage-jobs" className="view-all">
                            Manage Jobs
                        </Link>
                    </div>

                    <div className="jobs-list">
                        {recent_jobs?.length > 0 ? (
                            recent_jobs.map((job) => (
                                <div key={job.id} className="job-item">
                                    <div className="job-info">
                                        <h4>{job.title}</h4>
                                        <div className="job-meta">
                                            <span>
                                                <i className="fas fa-dollar-sign"></i>
                                                ${job.pay_per_hour}/hr
                                            </span>
                                            <span>
                                                <i className="fas fa-users"></i>
                                                {job.applications_count || 0} applicants
                                            </span>
                                            <span className={`status-badge ${job.is_active ? 'active' : 'inactive'}`}>
                                                {job.is_active ? 'Active' : 'Closed'}
                                            </span>
                                        </div>
                                    </div>
                                    <Link to={`/jobs/${job.id}/applications`} className="btn btn-outline btn-small">
                                        View Applications
                                    </Link>
                                </div>
                            ))
                        ) : (
                            <div className="empty-state">
                                <i className="fas fa-briefcase"></i>
                                <p>No jobs posted yet</p>
                                <Link to="/post-job" className="btn btn-primary">
                                    Post Your First Job
                                </Link>
                            </div>
                        )}
                    </div>
                </div>

                {/* Recent Applications */}
                <div className="dashboard-card recent-applications">
                    <div className="card-header">
                        <h3>
                            <i className="fas fa-file-alt"></i>
                            Recent Applications
                        </h3>
                        <Link to="/applications" className="view-all">
                            View All
                        </Link>
                    </div>

                    <div className="applications-list">
                        {recent_applications?.length > 0 ? (
                            recent_applications.map((app) => (
                                <div key={app.id} className="application-item">
                                    <div className="application-info">
                                        <h4>{app.freelancer_name}</h4>
                                        <p className="job-title">Applied for: {app.job_title}</p>
                                        <div className="application-meta">
                                            <span className="applied-date">
                                                {new Date(app.applied_at).toLocaleDateString()}
                                            </span>
                                            <span className={`status-badge ${app.status}`}>
                                                {app.status}
                                            </span>
                                        </div>
                                    </div>
                                    <Link
                                        to={`/jobs/${app.job_id}/applications?application=${app.id}`}
                                        className="btn btn-outline btn-small"
                                    >
                                        Review
                                    </Link>
                                </div>
                            ))
                        ) : (
                            <div className="empty-state">
                                <i className="fas fa-file-alt"></i>
                                <p>No applications yet</p>
                                <p className="hint">Applications will appear here when freelancers apply to your jobs</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Notifications */}
                <div className="dashboard-card notifications">
                    <div className="card-header">
                        <h3>
                            <i className="fas fa-bell"></i>
                            Recent Notifications
                        </h3>
                        <Link to="/notifications" className="view-all">
                            View All
                        </Link>
                    </div>

                    <div className="notifications-list">
                        {notifications?.length > 0 ? (
                            notifications.map((notification) => (
                                <div key={notification.id} className={`notification-item ${!notification.is_read ? 'unread' : ''}`}>
                                    <div className="notification-icon">
                                        <i className="fas fa-bell"></i>
                                    </div>
                                    <div className="notification-content">
                                        <h4>{notification.title}</h4>
                                        <p>{notification.message}</p>
                                        <span className="notification-time">
                                            {new Date(notification.created_at).toLocaleDateString()}
                                        </span>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="empty-state">
                                <i className="fas fa-bell-slash"></i>
                                <p>No notifications</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Quick Stats */}
                <div className="dashboard-card quick-stats">
                    <div className="card-header">
                        <h3>
                            <i className="fas fa-chart-line"></i>
                            Hiring Insights
                        </h3>
                    </div>

                    <div className="stats-insights">
                        <div className="insight-item">
                            <div className="insight-label">
                                <span>Application Rate</span>
                                <span className="insight-value">
                                    {stats?.total_jobs ? ((stats?.total_applications / stats?.total_jobs) || 0).toFixed(1) : 0}/job
                                </span>
                            </div>
                            <div className="progress-bar">
                                <div
                                    className="progress-fill"
                                    style={{ width: `${Math.min((stats?.total_applications / (stats?.total_jobs * 10)) * 100, 100)}%` }}
                                ></div>
                            </div>
                        </div>

                        <div className="insight-item">
                            <div className="insight-label">
                                <span>Acceptance Rate</span>
                                <span className="insight-value">
                                    {stats?.total_applications ?
                                        ((stats?.accepted_applications / stats?.total_applications) * 100 || 0).toFixed(1) : 0}%
                                </span>
                            </div>
                            <div className="progress-bar">
                                <div
                                    className="progress-fill success"
                                    style={{ width: `${stats?.total_applications ? (stats?.accepted_applications / stats?.total_applications) * 100 : 0}%` }}
                                ></div>
                            </div>
                        </div>

                        <div className="stats-summary">
                            <div className="summary-item">
                                <span className="summary-label">Company Profile</span>
                                <span className={`summary-status ${profile?.is_verified ? 'verified' : 'pending'}`}>
                                    {profile?.is_verified ? 'Verified' : 'Pending Verification'}
                                </span>
                            </div>
                            <div className="summary-item">
                                <span className="summary-label">Account Created</span>
                                <span className="summary-value">
                                    {new Date(profile?.created_at).toLocaleDateString()}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RecruiterDashboard;