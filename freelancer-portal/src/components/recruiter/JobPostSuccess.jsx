// src/components/recruiter/JobPostSuccess.jsx
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import '../../styles/JobPostSuccess.css';

const JobPostSuccess = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { job, message } = location.state || {};

    if (!job) {
        navigate('/recruiter/dashboard');
        return null;
    }

    const copyToClipboard = () => {
        const jobUrl = `${window.location.origin}/freelancer/jobs/${job.id}`;
        navigator.clipboard.writeText(jobUrl);
        toast.success('Job link copied to clipboard!');
    };

    const shareOnLinkedIn = () => {
        const url = encodeURIComponent(`${window.location.origin}/freelancer/jobs/${job.id}`);
        const title = encodeURIComponent(`Hiring: ${job.title} at ${job.company}`);
        window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}&title=${title}`, '_blank');
    };

    const shareOnTwitter = () => {
        const url = encodeURIComponent(`${window.location.origin}/freelancer/jobs/${job.id}`);
        const text = encodeURIComponent(`We're hiring! Check out this opportunity: ${job.title} at ${job.company}`);
        window.open(`https://twitter.com/intent/tweet?text=${text}&url=${url}`, '_blank');
    };

    return (
        <div className="job-post-success-container">
            <div className="success-card">
                <div className="success-icon">✅</div>
                <h1>Job Posted Successfully!</h1>
                <p className="success-message">{message || 'Your job has been published and is now live.'}</p>

                <div className="job-summary">
                    <h2>Job Details</h2>
                    <div className="job-info">
                        <div className="info-row">
                            <strong>Title:</strong> <span>{job.title}</span>
                        </div>
                        <div className="info-row">
                            <strong>Company:</strong> <span>{job.company}</span>
                        </div>
                        <div className="info-row">
                            <strong>Location:</strong> <span>{job.location}</span>
                        </div>
                        <div className="info-row">
                            <strong>Job Type:</strong> <span>{job.jobType}</span>
                        </div>
                        {job.salary && (
                            <div className="info-row">
                                <strong>Salary:</strong> <span>${job.salary.min} - ${job.salary.max}</span>
                            </div>
                        )}
                    </div>
                </div>

                <div className="action-buttons">
                    <button onClick={copyToClipboard} className="action-btn copy-btn">
                        📋 Copy Job Link
                    </button>
                    <button onClick={shareOnLinkedIn} className="action-btn linkedin-btn">
                        🔗 Share on LinkedIn
                    </button>
                    <button onClick={shareOnTwitter} className="action-btn twitter-btn">
                        🐦 Share on Twitter
                    </button>
                </div>

                <div className="navigation-buttons">
                    <button onClick={() => navigate('/recruiter/jobs')} className="nav-btn manage-btn">
                        View All Jobs
                    </button>
                    <button onClick={() => navigate('/recruiter/post-job')} className="nav-btn post-another-btn">
                        Post Another Job
                    </button>
                    <button onClick={() => navigate('/recruiter/dashboard')} className="nav-btn dashboard-btn">
                        Go to Dashboard
                    </button>
                </div>
            </div>
        </div>
    );
};

export default JobPostSuccess;