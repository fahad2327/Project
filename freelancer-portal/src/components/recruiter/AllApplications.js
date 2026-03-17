import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import recruiterService from '../../services/recruiterService';
import Loader from '../common/Loader';
import toast from 'react-hot-toast';
import './Recruiter.css';

const AllApplications = () => {
    const [applications, setApplications] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchAllApplications();
    }, []);

    const fetchAllApplications = async () => {
        try {
            const response = await recruiterService.getAllApplications();
            if (response.success) {
                setApplications(response.applications);
            }
        } catch (error) {
            toast.error('Failed to load applications');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <Loader />;

    return (
        <div className="all-applications-container">
            <h1>All Applications</h1>
            {applications.length === 0 ? (
                <div className="empty-state">
                    <i className="fas fa-file-alt"></i>
                    <p>No applications received yet.</p>
                </div>
            ) : (
                <div className="applications-grid">
                    {applications.map((app) => (
                        <div key={app.id} className="application-card">
                            <div className="applicant-header">
                                <div className="applicant-avatar">{app.freelancer_name?.charAt(0)}</div>
                                <div className="applicant-info">
                                    <h3>{app.freelancer_name}</h3>
                                    <p className="applicant-email">{app.freelancer_email}</p>
                                </div>
                                <span className={`status-badge ${app.status}`}>{app.status}</span>
                            </div>

                            <div className="applicant-details">
                                <div className="detail-row">
                                    <span className="detail-label">Job:</span>
                                    <span className="detail-value">{app.job_title}</span>
                                </div>
                                <div className="detail-row">
                                    <span className="detail-label"><i className="fas fa-dollar-sign"></i> Proposed Rate:</span>
                                    <span className="detail-value">${app.proposed_rate || 'Not specified'}/hr</span>
                                </div>
                                <div className="detail-row">
                                    <span className="detail-label"><i className="fas fa-calendar"></i> Applied:</span>
                                    <span className="detail-value">{new Date(app.applied_at).toLocaleDateString()}</span>
                                </div>
                            </div>

                            {app.cover_letter && (
                                <div className="cover-letter">
                                    <h4>Cover Letter</h4>
                                    <p>{app.cover_letter}</p>
                                </div>
                            )}

                            <div className="application-actions">
                                <Link
                                    to={`/recruiter/jobs/${app.job_id}/applications?application=${app.id}`}
                                    className="btn btn-primary btn-small"
                                >
                                    Review
                                </Link>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default AllApplications;