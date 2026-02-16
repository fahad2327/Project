import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import freelancerService from '../../services/freelancerService';
import Loader from '../common/Loader';
import './Freelancer.css';

const MyApplications = () => {
    const [applications, setApplications] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchApplications();
    }, []);

    const fetchApplications = async () => {
        try {
            const response = await freelancerService.getApplications();
            if (response.success) {
                setApplications(response.applications);
            }
        } catch (error) {
            console.error('Failed to fetch applications:', error);
        } finally {
            setLoading(false);
        }
    };

    const getStatusColor = (status) => {
        const colors = {
            applied: 'info',
            reviewed: 'warning',
            shortlisted: 'success',
            accepted: 'success',
            rejected: 'danger'
        };
        return colors[status] || 'secondary';
    };

    if (loading) return <Loader />;

    return (
        <div className="my-applications-container">
            <h1>My Applications</h1>

            {applications.length === 0 ? (
                <div className="empty-state">
                    <i className="fas fa-file-alt"></i>
                    <h3>No applications yet</h3>
                    <p>Browse jobs and start applying to opportunities</p>
                    <Link to="/jobs" className="btn btn-primary">
                        Browse Jobs
                    </Link>
                </div>
            ) : (
                <div className="applications-grid">
                    {applications.map((app) => (
                        <div key={app.id} className="application-card">
                            <div className="application-header">
                                <h3>{app.title}</h3>
                                <span className={`status-badge ${app.status}`}>
                                    {app.status}
                                </span>
                            </div>

                            <p className="company-name">{app.company_name}</p>

                            <div className="application-details">
                                <div className="detail">
                                    <i className="fas fa-dollar-sign"></i>
                                    <span>${app.pay_per_hour}/hr</span>
                                </div>
                                <div className="detail">
                                    <i className="fas fa-calendar"></i>
                                    <span>Applied: {new Date(app.applied_at).toLocaleDateString()}</span>
                                </div>
                            </div>

                            {app.recruiter_notes && (
                                <div className="recruiter-notes">
                                    <strong>Recruiter Notes:</strong>
                                    <p>{app.recruiter_notes}</p>
                                </div>
                            )}

                            <div className="application-footer">
                                <Link to={`/jobs/${app.job_id}`} className="btn btn-outline btn-small">
                                    View Job
                                </Link>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default MyApplications;