import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ isAuthenticated, onLogout, user }) => {
    const navigate = useNavigate();
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const handleLogout = () => {
        onLogout();
        navigate('/signin');
        setIsMenuOpen(false);
    };

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/" className="navbar-logo">
                    <span className="logo-text">FreelancerPortal</span>
                </Link>

                <div className="menu-icon" onClick={toggleMenu}>
                    <i className={isMenuOpen ? 'fas fa-times' : 'fas fa-bars'}></i>
                </div>

                <div className={`nav-menu ${isMenuOpen ? 'active' : ''}`}>
                    {isAuthenticated ? (
                        <>
                            <Link to="/welcome" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                                <i className="fas fa-home"></i>
                                Dashboard
                            </Link>
                            <div className="user-menu">
                                <span className="user-name">
                                    <i className="fas fa-user-circle"></i>
                                    {user?.name || 'User'}
                                </span>
                                <button onClick={handleLogout} className="logout-btn">
                                    <i className="fas fa-sign-out-alt"></i>
                                    Logout
                                </button>
                            </div>
                        </>
                    ) : (
                        <>
                            <Link to="/signin" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                                <i className="fas fa-sign-in-alt"></i>
                                Sign In
                            </Link>
                            <Link to="/signup" className="nav-link" onClick={() => setIsMenuOpen(false)}>
                                <i className="fas fa-user-plus"></i>
                                Sign Up
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;