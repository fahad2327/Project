import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import notificationService from '../../services/notificationService';
import './Navbar.css';

const Navbar = () => {
    const { isAuthenticated, user, userRole, logout } = useAuth();
    const navigate = useNavigate();
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
    const [unreadCount, setUnreadCount] = useState(0);
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    useEffect(() => {
        if (isAuthenticated) {
            fetchUnreadCount();
            // Poll for new notifications every 30 seconds
            const interval = setInterval(fetchUnreadCount, 30000);
            return () => clearInterval(interval);
        }
    }, [isAuthenticated]);

    const fetchUnreadCount = async () => {
        try {
            const response = await notificationService.getUnreadCount();
            setUnreadCount(response.unread_count);
        } catch (error) {
            console.error('Failed to fetch unread count:', error);
        }
    };

    const handleLogout = async () => {
        await logout();
        navigate('/');
        setIsMenuOpen(false);
        setIsProfileMenuOpen(false);
    };

    const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
    const toggleProfileMenu = () => setIsProfileMenuOpen(!isProfileMenuOpen);

    const getDashboardLink = () => {
        return userRole === 'recruiter' ? '/dashboard' : '/dashboard';
    };

    const navLinks = isAuthenticated ? (
        userRole === 'freelancer' ? (
            <>
                <Link to="/jobs" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                    Find Jobs
                </Link>
                <Link to="/my-applications" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                    My Applications
                </Link>
            </>
        ) : (
            <>
                <Link to="/post-job" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                    Post Job
                </Link>
                <Link to="/manage-jobs" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                    Manage Jobs
                </Link>
            </>
        )
    ) : (
        <>
            <Link to="/jobs" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                Find Work
            </Link>
            <Link to="/post-job" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                Post a Job
            </Link>
        </>
    );

    return (
        <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
            <div className="navbar-container">
                <Link to="/" className="navbar-logo">
                    <span className="logo-icon">⚡</span>
                    <span className="logo-text">FreelanceHub</span>
                </Link>

                <div className="menu-icon" onClick={toggleMenu}>
                    <div className={`hamburger ${isMenuOpen ? 'active' : ''}`}>
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>

                <div className={`nav-menu ${isMenuOpen ? 'active' : ''}`}>
                    <div className="nav-links">
                        {navLinks}
                    </div>

                    <div className="nav-actions">
                        {isAuthenticated ? (
                            <>
                                <Link to="/notifications" className="notification-badge">
                                    <i className="fas fa-bell"></i>
                                    {unreadCount > 0 && (
                                        <span className="badge">{unreadCount}</span>
                                    )}
                                </Link>

                                <div className="profile-menu-container">
                                    <button className="profile-button" onClick={toggleProfileMenu}>
                                        <div className="profile-avatar">
                                            {user?.first_name?.[0]}{user?.last_name?.[0]}
                                        </div>
                                        <span className="profile-name">
                                            {user?.first_name} {user?.last_name}
                                        </span>
                                        <i className={`fas fa-chevron-${isProfileMenuOpen ? 'up' : 'down'}`}></i>
                                    </button>

                                    {isProfileMenuOpen && (
                                        <div className="profile-dropdown">
                                            <Link to="/dashboard" onClick={() => setIsProfileMenuOpen(false)}>
                                                <i className="fas fa-tachometer-alt"></i>
                                                Dashboard
                                            </Link>
                                            <Link to="/profile" onClick={() => setIsProfileMenuOpen(false)}>
                                                <i className="fas fa-user"></i>
                                                Profile
                                            </Link>
                                            <Link to="/settings" onClick={() => setIsProfileMenuOpen(false)}>
                                                <i className="fas fa-cog"></i>
                                                Settings
                                            </Link>
                                            <div className="dropdown-divider"></div>
                                            <button onClick={handleLogout}>
                                                <i className="fas fa-sign-out-alt"></i>
                                                Logout
                                            </button>
                                        </div>
                                    )}
                                </div>
                            </>
                        ) : (
                            <div className="auth-buttons">
                                <Link to="/login" className="btn btn-outline btn-small">
                                    Sign In
                                </Link>
                                <Link to="/register" className="btn btn-primary btn-small">
                                    Sign Up
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;