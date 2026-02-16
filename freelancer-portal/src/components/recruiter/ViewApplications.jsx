import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import recruiterService from '../../services/recruiterService';
import toast from 'react-hot-toast';
import Loader from '../common/Loader';
import './Recruiter.css';

const ViewApplications = () => {
    const { jobId } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [applications, setApplications] = useState([]);
    const [job, setJob] = useState(null);
    const [selectedApplication, setSelectedApplication] = useState(null);
    const [statusUpdate, setStatusUpdate] = useState('');
    const [recruiterNotes, setRecruiterNotes] = useState('');

    useEffect(() => {
        fetchApplications();
    }, [jobId]);

    const fetchApplications = async () => {
        setLoading(true);
        try {
            const response = await recruiterService.getJobApplications(jobId);
            if (response.success) {
                setApplications(response.applications);
                setJob(response.applications[0]?.job_title ? { title: response.applications[0].job_title } : null);
            }
        } catch (error) {
            console.error('Failed to fetch applications:', error);
            toast.error('Failed to load applications');
        } finally {
            setLoading(false);
        }
    };

    const handleStatusUpdate = async (applicationId) => {
        if (!statusUpdate) {
            toast.error('Please select a status');
            return;
        }

        try {
            const response = await recruiterService.updateApplicationStatus(applicationId, {
                status: statusUpdate,
                recruiter_notes: recruiterNotes
            });

            if (response.success) {
                toast.success(`Application ${statusUpdate} successfully`);
                setSelectedApplication(null);
                setStatusUpdate('');
                setRecruiterNotes('');
                fetchApplications();
            }
        } catch (error) {
            console.error('Failed to update status:', error);
            toast.error('Failed to update application status');
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
        <div className="view-applications-container">
            <div className="applications-header">
                <div className="header-left">
                    <button onClick={() => navigate('/manage-jobs')} className="back-button">
                        <i className="fas fa-arrow-left"></i>
                        Back to Jobs
                    </button>
                    <h1>{job?.title || 'Job Applications'}</h1>
                </div>
                <div className="applications-stats">
                    <div className="stat">
                        <span className="stat-value">{applications.length}</span>
                        <span className="stat-label">Total</span>
                    </div>
                    <div className="stat">
                        <span className="stat-value">
                            {applications.filter(a => a.status === 'pending').length}
                        </span>
                        <span className="stat-label">Pending</span>
                    </div>
                    <div className="stat">
                        <span className="stat-value">
                            {applications.filter(a => a.status === 'shortlisted').length}
                        </span>
                        <span className="stat-label">Shortlisted</span>
                    </div>
                </div>
            </div>

            {applications.length === 0 ? (
                <div className="no-applications">
                    <i className="fas fa-users"></i>
                    <h3>No applications yet</h3>
                    <p>When freelancers apply for this job, they will appear here.</p>
                    <button onClick={() => navigate('/manage-jobs')} className="btn btn-outline">
                        Back to Jobs
                    </button>
                </div>
            ) : (
                <div className="applications-grid">
                    {applications.map((app) => (
                        <div key={app.id} className="application-card">
                            <div className="applicant-header">
                                <div className="applicant-avatar">
                                    {app.freelancer_name?.charAt(0)}
                                </div>
                                <div className="applicant-info">
                                    <h3>{app.freelancer_name}</h3>
                                    <p className="applicant-email">{app.freelancer_email}</p>
                                </div>
                                <span className={`status-badge ${app.status}`}>
                                    {app.status}
                                </span>
                            </div>

                            <div className="applicant-details">
                                <div className="detail-row">
                                    <span className="detail-label">
                                        <i className="fas fa-dollar-sign"></i>
                                        Proposed Rate:
                                    </span>
                                    <span className="detail-value">
                                        ${app.proposed_rate || 'Not specified'}/hr
                                    </span>
                                </div>
                                <div className="detail-row">
                                    <span className="detail-label">
                                        <i className="fas fa-calendar"></i>
                                        Availability:
                                    </span>
                                    <span className="detail-value">
                                        {app.availability_date ? new Date(app.availability_date).toLocaleDateString() : 'Immediate'}
                                    </span>
                                </div>
                                <div className="detail-row">
                                    <span className="detail-label">
                                        <i className="fas fa-clock"></i>
                                        Applied:
                                    </span>
                                    <span className="detail-value">
                                        {new Date(app.applied_at).toLocaleDateString()}
                                    </span>
                                </div>
                            </div>

                            {app.cover_letter && (
                                <div className="cover-letter">
                                    <h4>Cover Letter</h4>
                                    <p>{app.cover_letter}</p>
                                </div>
                            )}

                            {app.skills && app.skills.length > 0 && (
                                <div className="applicant-skills">
                                    <h4>Skills</h4>
                                    <div className="skills-list">
                                        {app.skills.map((skill, index) => (
                                            <span key={index} className="skill-badge">{skill}</span>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {selectedApplication === app.id ? (
                                <div className="status-update-form">
                                    <h4>Update Application Status</h4>
                                    <select
                                        value={statusUpdate}
                                        onChange={(e) => setStatusUpdate(e.target.value)}
                                        className="status-select"
                                    >
                                        <option value="">Select Status</option>
                                        <option value="reviewed">Mark as Reviewed</option>
                                        <option value="shortlisted">Shortlist</option>
                                        <option value="accepted">Accept</option>
                                        <option value="rejected">Reject</option>
                                    </select>
                                    <textarea
                                        value={recruiterNotes}
                                        onChange={(e) => setRecruiterNotes(e.target.value)}
                                        placeholder="Add notes (optional)"
                                        rows="3"
                                    />
                                    <div className="form-actions">
                                        <button
                                            onClick={() => handleStatusUpdate(app.id)}
                                            className="btn btn-primary"
                                        >
                                            Update Status
                                        </button>
                                        <button
                                            onClick={() => setSelectedApplication(null)}
                                            className="btn btn-outline"
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                </div>
                            ) : (
                                <div className="application-actions">
                                    <button
                                        onClick={() => setSelectedApplication(app.id)}
                                        className="btn btn-primary"
                                    >
                                        Update Status
                                    </button>
                                    <button className="btn btn-outline">
                                        <i className="fas fa-download"></i>
                                        Resume
                                    </button>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ViewApplications;