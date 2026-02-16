import React from 'react';
import { Link } from 'react-router-dom';
import './Welcome.css';

const Welcome = ({ user }) => {
    return (
        <div className="welcome-container">
            <div className="welcome-content">
                <h1>Welcome, {user?.name || 'Freelancer'}!</h1>
                <p>Your freelancer dashboard is ready</p>

                <div className="welcome-stats">
                    <div className="stat-card">
                        <i className="fas fa-project-diagram"></i>
                        <h3>0</h3>
                        <p>Active Projects</p>
                    </div>
                    <div className="stat-card">
                        <i className="fas fa-dollar-sign"></i>
                        <h3>$0</h3>
                        <p>Earnings</p>
                    </div>
                    <div className="stat-card">
                        <i className="fas fa-clock"></i>
                        <h3>0</h3>
                        <p>Hours Logged</p>
                    </div>
                </div>

                <div className="welcome-actions">
                    <Link to="/projects" className="action-button">
                        <i className="fas fa-search"></i>
                        Find Work
                    </Link>
                    <Link to="/profile" className="action-button secondary">
                        <i className="fas fa-user"></i>
                        Complete Profile
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default Welcome;