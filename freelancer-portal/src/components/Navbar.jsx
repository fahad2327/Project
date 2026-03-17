// import React, { useState, useEffect } from 'react';
// import { Link, useNavigate } from 'react-router-dom';
// import { useAuth } from '../../context/AuthContext';
// import notificationService from '../../services/notificationService';
// import './Navbar.css';

// const Navbar = () => {
//     const { isAuthenticated, user, userRole, logout } = useAuth();
//     const navigate = useNavigate();
//     const [isMenuOpen, setIsMenuOpen] = useState(false);
//     const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
//     const [unreadCount, setUnreadCount] = useState(0);
//     const [scrolled, setScrolled] = useState(false);

//     useEffect(() => {
//         const handleScroll = () => {
//             setScrolled(window.scrollY > 20);
//         };
//         window.addEventListener('scroll', handleScroll);
//         return () => window.removeEventListener('scroll', handleScroll);
//     }, []);

//     useEffect(() => {
//         if (isAuthenticated) {
//             fetchUnreadCount();
//             // Poll for new notifications every 30 seconds
//             const interval = setInterval(fetchUnreadCount, 30000);
//             return () => clearInterval(interval);
//         }
//     }, [isAuthenticated]);

//     const fetchUnreadCount = async () => {
//         try {
//             const response = await notificationService.getUnreadCount();
//             if (response?.success) {
//                 setUnreadCount(response.unread_count || 0);
//             }
//         } catch (error) {
//             console.error('Failed to fetch unread count:', error);
//         }
//     };

//     const handleLogout = async () => {
//         await logout();
//         navigate('/');
//         setIsMenuOpen(false);
//         setIsProfileMenuOpen(false);
//     };

//     const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
//     const toggleProfileMenu = () => setIsProfileMenuOpen(!isProfileMenuOpen);

//     const getDashboardLink = () => {
//         return userRole === 'recruiter' ? '/recruiter/dashboard' : '/freelancer/dashboard';
//     };

//     const getInitials = () => {
//         if (user?.first_name && user?.last_name) {
//             return `${user.first_name[0]}${user.last_name[0]}`;
//         }
//         return user?.email?.[0] || 'U';
//     };

//     return (
//         <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
//             <div className="navbar-container">
//                 <Link to="/" className="navbar-logo">
//                     <span className="logo-icon">⚡</span>
//                     <span className="logo-text">FreelanceHub</span>
//                 </Link>

//                 <div className="menu-icon" onClick={toggleMenu}>
//                     <div className={`hamburger ${isMenuOpen ? 'active' : ''}`}>
//                         <span></span>
//                         <span></span>
//                         <span></span>
//                     </div>
//                 </div>

//                 <div className={`nav-menu ${isMenuOpen ? 'active' : ''}`}>
//                     <div className="nav-links">
//                         {isAuthenticated ? (
//                             <>
//                                 <Link to={getDashboardLink()} className="nav-link" onClick={() => setIsMenuOpen(false)}>
//                                     <i className="fas fa-home"></i>
//                                     Dashboard
//                                 </Link>

//                                 {userRole === 'freelancer' ? (
//                                     <>
//                                         <Link to="/jobs" className="nav-link" onClick={() => setIsMenuOpen(false)}>
//                                             <i className="fas fa-search"></i>
//                                             Find Jobs
//                                         </Link>
//                                         <Link to="/my-applications" className="nav-link" onClick={() => setIsMenuOpen(false)}>
//                                             <i className="fas fa-file-alt"></i>
//                                             My Applications
//                                         </Link>
//                                     </>
//                                 ) : (
//                                     <>
//                                         <Link to="/post-job" className="nav-link" onClick={() => setIsMenuOpen(false)}>
//                                             <i className="fas fa-plus-circle"></i>
//                                             Post Job
//                                         </Link>
//                                         <Link to="/manage-jobs" className="nav-link" onClick={() => setIsMenuOpen(false)}>
//                                             <i className="fas fa-briefcase"></i>
//                                             Manage Jobs
//                                         </Link>
//                                     </>
//                                 )}

//                                 <Link to="/profile" className="nav-link" onClick={() => setIsMenuOpen(false)}>
//                                     <i className="fas fa-user"></i>
//                                     Profile
//                                 </Link>
//                             </>
//                         ) : (
//                             <>
//                                 <Link to="/jobs" className="nav-link" onClick={() => setIsMenuOpen(false)}>
//                                     <i className="fas fa-search"></i>
//                                     Find Work
//                                 </Link>
//                                 <Link to="/post-job" className="nav-link" onClick={() => setIsMenuOpen(false)}>
//                                     <i className="fas fa-briefcase"></i>
//                                     Post a Job
//                                 </Link>
//                             </>
//                         )}
//                     </div>

//                     <div className="nav-actions">
//                         {isAuthenticated ? (
//                             <>
//                                 <Link to="/notifications" className="notification-badge">
//                                     <i className="fas fa-bell"></i>
//                                     {unreadCount > 0 && (
//                                         <span className="badge">{unreadCount}</span>
//                                     )}
//                                 </Link>

//                                 <div className="profile-menu-container">
//                                     <button className="profile-button" onClick={toggleProfileMenu}>
//                                         <div className="profile-avatar">
//                                             {getInitials()}
//                                         </div>
//                                         <span className="profile-name">
//                                             {user?.first_name || user?.name || 'User'}
//                                         </span>
//                                         <i className={`fas fa-chevron-${isProfileMenuOpen ? 'up' : 'down'}`}></i>
//                                     </button>

//                                     {isProfileMenuOpen && (
//                                         <div className="profile-dropdown">
//                                             <Link to={getDashboardLink()} onClick={() => setIsProfileMenuOpen(false)}>
//                                                 <i className="fas fa-tachometer-alt"></i>
//                                                 Dashboard
//                                             </Link>
//                                             <Link to="/profile" onClick={() => setIsProfileMenuOpen(false)}>
//                                                 <i className="fas fa-user"></i>
//                                                 Profile
//                                             </Link>
//                                             <Link to="/settings" onClick={() => setIsProfileMenuOpen(false)}>
//                                                 <i className="fas fa-cog"></i>
//                                                 Settings
//                                             </Link>
//                                             <div className="dropdown-divider"></div>
//                                             <button onClick={handleLogout}>
//                                                 <i className="fas fa-sign-out-alt"></i>
//                                                 Logout
//                                             </button>
//                                         </div>
//                                     )}
//                                 </div>
//                             </>
//                         ) : (
//                             <div className="auth-buttons">
//                                 <Link to="/login" className="btn btn-outline btn-small" onClick={() => setIsMenuOpen(false)}>
//                                     Sign In
//                                 </Link>
//                                 <Link to="/register" className="btn btn-primary btn-small" onClick={() => setIsMenuOpen(false)}>
//                                     Sign Up
//                                 </Link>
//                             </div>
//                         )}
//                     </div>
//                 </div>
//             </div>
//         </nav>
//     );
// };

// export default Navbar;
// src/components/Navbar.jsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import NotificationBell from './NotificationBell';
import './Navbar.css';

const Navbar = () => {
    const { user, userRole, logout } = useAuth();
    const navigate = useNavigate();
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const handleLogout = async () => {
        await logout();
        navigate('/');
        setIsMenuOpen(false);
        setIsProfileMenuOpen(false);
    };

    const getInitials = () => {
        if (user?.first_name && user?.last_name) {
            return `${user.first_name[0]}${user.last_name[0]}`;
        }
        if (user?.name) {
            return user.name.split(' ').map(n => n[0]).join('').substring(0, 2);
        }
        return user?.email?.[0]?.toUpperCase() || 'U';
    };

    const getDashboardLink = () => {
        if (!userRole) return '/dashboard';
        return userRole === 'recruiter' ? '/recruiter/dashboard' : '/freelancer/dashboard';
    };

    return (
        <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
            <div className="navbar-container">
                <Link to="/" className="navbar-logo">
                    <span className="logo-icon">⚡</span>
                    <span className="logo-text">FreelanceHub</span>
                </Link>

                <div className="menu-icon" onClick={() => setIsMenuOpen(!isMenuOpen)}>
                    <div className={`hamburger ${isMenuOpen ? 'active' : ''}`}>
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>

                <div className={`nav-menu ${isMenuOpen ? 'active' : ''}`}>
                    <div className="nav-links">
                        {user ? (
                            <>
                                <Link to={getDashboardLink()} className="nav-link" onClick={() => setIsMenuOpen(false)}>
                                    <i className="fas fa-home"></i> Dashboard
                                </Link>

                                {userRole === 'freelancer' ? (
                                    <>
                                        <Link to="/jobs" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                                            <i className="fas fa-search"></i> Find Jobs
                                        </Link>
                                        <Link to="/my-applications" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                                            <i className="fas fa-file-alt"></i> My Applications
                                        </Link>
                                    </>
                                ) : userRole === 'recruiter' ? (
                                    <>
                                        <Link to="/post-job" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                                            <i className="fas fa-plus-circle"></i> Post Job
                                        </Link>
                                        <Link to="/manage-jobs" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                                            <i className="fas fa-briefcase"></i> Manage Jobs
                                        </Link>
                                    </>
                                ) : null}
                            </>
                        ) : (
                            <>
                                <Link to="/jobs" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                                    <i className="fas fa-search"></i> Find Work
                                </Link>
                                <Link to="/post-job" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                                    <i className="fas fa-briefcase"></i> Post a Job
                                </Link>
                            </>
                        )}
                    </div>

                    <div className="nav-actions">
                        {user ? (
                            <>
                                <NotificationBell />

                                <div className="profile-menu-container">
                                    <button
                                        className="profile-button"
                                        onClick={() => setIsProfileMenuOpen(!isProfileMenuOpen)}
                                    >
                                        <div className="profile-avatar">
                                            {getInitials()}
                                        </div>
                                        <span className="profile-name">
                                            {user?.first_name || user?.name?.split(' ')[0] || 'User'}
                                        </span>
                                        <i className={`fas fa-chevron-${isProfileMenuOpen ? 'up' : 'down'}`}></i>
                                    </button>

                                    {isProfileMenuOpen && (
                                        <div className="profile-dropdown">
                                            <Link to={getDashboardLink()} onClick={() => setIsProfileMenuOpen(false)}>
                                                <i className="fas fa-tachometer-alt"></i> Dashboard
                                            </Link>
                                            <Link to="/profile" onClick={() => setIsProfileMenuOpen(false)}>
                                                <i className="fas fa-user"></i> Profile
                                            </Link>
                                            <Link to="/settings" onClick={() => setIsProfileMenuOpen(false)}>
                                                <i className="fas fa-cog"></i> Settings
                                            </Link>
                                            <div className="dropdown-divider"></div>
                                            <button onClick={handleLogout}>
                                                <i className="fas fa-sign-out-alt"></i> Logout
                                            </button>
                                        </div>
                                    )}
                                </div>
                            </>
                        ) : (
                            <div className="auth-buttons">
                                <Link to="/login" className="btn btn-outline" onClick={() => setIsMenuOpen(false)}>
                                    Sign In
                                </Link>
                                <Link to="/register" className="btn btn-primary" onClick={() => setIsMenuOpen(false)}>
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