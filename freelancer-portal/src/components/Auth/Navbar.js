import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { FaUser, FaSignOutAlt, FaBriefcase } from 'react-icons/fa';

function Navbar() {
    const { currentUser, signout } = useAuth();
    const navigate = useNavigate();

    const handleSignout = () => {
        signout();
        navigate('/');
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="container">
                <Link className="navbar-brand d-flex align-items-center" to="/">
                    <FaBriefcase className="me-2" />
                    <span className="fw-bold">Freelancer Portal</span>
                </Link>

                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav ms-auto">
                        {currentUser ? (
                            <>
                                <li className="nav-item">
                                    <span className="nav-link text-light">
                                        <FaUser className="me-1" />
                                        Welcome, {currentUser.name}
                                    </span>
                                </li>
                                <li className="nav-item">
                                    <button
                                        className="btn btn-outline-light ms-2"
                                        onClick={handleSignout}
                                    >
                                        <FaSignOutAlt className="me-1" />
                                        Sign Out
                                    </button>
                                </li>
                            </>
                        ) : (
                            <>
                                <li className="nav-item">
                                    <Link className="btn btn-outline-light me-2" to="/signin">
                                        Sign In
                                    </Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="btn btn-warning" to="/signup">
                                        Sign Up
                                    </Link>
                                </li>
                            </>
                        )}
                    </ul>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;