import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import freelancerService from '../../services/freelancerService';
import notificationService from '../../services/notificationService';
import Loader from '../common/Loader';
import './Freelancer.css';

const FreelancerDashboard = () => {
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        fetchDashboardData();
        fetchNotifications();
    }, []);

    const fetchDashboardData = async () => {
        try {
            const response = await freelancerService.getDashboard();
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

    const { profile, stats, recent_applications, recommended_jobs } = dashboardData || {};

    return (
        <div className="freelancer-dashboard">
            {/* Welcome Section */}
            <div className="welcome-section">
                <div className="welcome-content">
                    <h1>
                        Welcome back, {profile?.first_name}! 👋
                    </h1>
                    <p>Here's what's happening with your freelance career today.</p>
                </div>
                <div className="profile-completion">
                    <div className="completion-circle">
                        <svg viewBox="0 0 36 36">
                            <path
                                d="M18 2.0845
                  a 15.9155 15.9155 0 0 1 0 31.831
                  a 15.9155 15.9155 0 0 1 0 -31.831"
                                fill="none"
                                stroke="var(--light-gray)"
                                strokeWidth="3"
                            />
                            <path
                                d="M18 2.0845
                  a 15.9155 15.9155 0 0 1 0 31.831
                  a 15.9155 15.9155 0 0 1 0 -31.831"
                                fill="none"
                                stroke="var(--primary-color)"
                                strokeWidth="3"
                                strokeDasharray={`${stats?.profile_completion || 0}, 100`}
                            />
                        </svg>
                        <span className="completion-percentage">
                            {stats?.profile_completion || 0}%
                        </span>
                    </div>
                    <div className="completion-text">
                        <h3>Profile Strength</h3>
                        <Link to="/profile" className="btn btn-outline btn-small">
                            Complete Profile
                        </Link>
                    </div>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-icon">
                        <i className="fas fa-briefcase"></i>
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

                <div className="stat-card">
                    <div className="stat-icon accepted">
                        <i className="fas fa-check-circle"></i>
                    </div>
                    <div className="stat-details">
                        <h3>{stats?.accepted_applications || 0}</h3>
                        <p>Accepted</p>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon rate">
                        <i className="fas fa-dollar-sign"></i>
                    </div>
                    <div className="stat-details">
                        <h3>${profile?.hourly_rate || 0}</h3>
                        <p>Hourly Rate</p>
                    </div>
                </div>
            </div>

            {/* Main Content Grid */}
            <div className="dashboard-grid">
                {/* Recent Applications */}
                <div className="dashboard-card recent-applications">
                    <div className="card-header">
                        <h3>
                            <i className="fas fa-file-alt"></i>
                            Recent Applications
                        </h3>
                        <Link to="/my-applications" className="view-all">
                            View All
                        </Link>
                    </div>

                    <div className="applications-list">
                        {recent_applications?.length > 0 ? (
                            recent_applications.map((app) => (
                                <div key={app.id} className="application-item">
                                    <div className="application-info">
                                        <h4>{app.title}</h4>
                                        <p className="company">{app.company_name}</p>
                                    </div>
                                    <div className="application-status">
                                        <span className={`status-badge ${app.status}`}>
                                            {app.status}
                                        </span>
                                        <span className="applied-date">
                                            {new Date(app.applied_at).toLocaleDateString()}
                                        </span>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="empty-state">
                                <i className="fas fa-file-alt"></i>
                                <p>No applications yet</p>
                                <Link to="/jobs" className="btn btn-primary">
                                    Browse Jobs
                                </Link>
                            </div>
                        )}
                    </div>
                </div>

                {/* Recommended Jobs */}
                <div className="dashboard-card recommended-jobs">
                    <div className="card-header">
                        <h3>
                            <i className="fas fa-star"></i>
                            Recommended for You
                        </h3>
                        <Link to="/jobs" className="view-all">
                            View All
                        </Link>
                    </div>

                    <div className="jobs-list">
                        {recommended_jobs?.length > 0 ? (
                            recommended_jobs.map((job) => (
                                <div key={job.id} className="job-item">
                                    <div className="job-info">
                                        <h4>{job.title}</h4>
                                        <p className="company">{job.company_name}</p>
                                        <div className="job-meta">
                                            <span>
                                                <i className="fas fa-dollar-sign"></i>
                                                ${job.pay_per_hour}/hr
                                            </span>
                                            <span>
                                                <i className="fas fa-briefcase"></i>
                                                {job.experience_level}
                                            </span>
                                            {job.is_remote && (
                                                <span className="remote-badge">
                                                    <i className="fas fa-globe"></i>
                                                    Remote
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                    <Link to={`/jobs/${job.id}`} className="btn btn-outline btn-small">
                                        View Job
                                    </Link>
                                </div>
                            ))
                        ) : (
                            <div className="empty-state">
                                <i className="fas fa-search"></i>
                                <p>No recommendations yet</p>
                                <p className="hint">Complete your profile to get personalized job recommendations</p>
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
                                        <i className={`fas fa-${notification.notification_type === 'application' ? 'file-alt' : 'bell'}`}></i>
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

                {/* Skills & Expertise */}
                <div className="dashboard-card skills-section">
                    <div className="card-header">
                        <h3>
                            <i className="fas fa-code"></i>
                            Your Skills
                        </h3>
                        <Link to="/profile" className="edit-link">
                            <i className="fas fa-edit"></i>
                            Edit
                        </Link>
                    </div>

                    <div className="skills-container">
                        {profile?.skills?.length > 0 ? (
                            profile.skills.map((skill) => (
                                <span key={skill.id} className="skill-tag">
                                    {skill.name}
                                    {skill.proficiency_level && (
                                        <span className="proficiency">{skill.proficiency_level}</span>
                                    )}
                                </span>
                            ))
                        ) : (
                            <div className="empty-state">
                                <p>No skills added yet</p>
                                <Link to="/profile" className="btn btn-outline btn-small">
                                    Add Skills
                                </Link>
                            </div>
                        )}
                    </div>

                    {profile?.tech_stacks?.length > 0 && (
                        <>
                            <h4 className="tech-stack-title">Tech Stack</h4>
                            <div className="tech-stack-container">
                                {profile.tech_stacks.map((tech) => (
                                    <span key={tech.id} className="tech-tag">
                                        {tech.name}
                                        {tech.experience_years && (
                                            <span className="experience">{tech.experience_years}y</span>
                                        )}
                                    </span>
                                ))}
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default FreelancerDashboard;