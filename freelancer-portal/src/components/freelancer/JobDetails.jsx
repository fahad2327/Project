import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import freelancerService from '../../services/freelancerService';
import toast from 'react-hot-toast';
import Loader from '../common/Loader';
import './Freelancer.css';

const JobDetails = () => {
    const { jobId } = useParams();
    const navigate = useNavigate();
    const [job, setJob] = useState(null);
    const [loading, setLoading] = useState(true);
    const [applying, setApplying] = useState(false);
    const [showApplicationForm, setShowApplicationForm] = useState(false);
    const [application, setApplication] = useState({
        cover_letter: '',
        proposed_rate: '',
        availability_date: ''
    });

    useEffect(() => {
        fetchJobDetails();
    }, [jobId]);

    const fetchJobDetails = async () => {
        try {
            const response = await freelancerService.getJobDetails(jobId);
            if (response.success) {
                setJob(response.job);
            }
        } catch (error) {
            console.error('Failed to fetch job details:', error);
            toast.error('Failed to load job details');
        } finally {
            setLoading(false);
        }
    };

    const handleApply = async (e) => {
        e.preventDefault();
        setApplying(true);
        try {
            const response = await freelancerService.applyForJob(jobId, application);
            if (response.success) {
                toast.success('Application submitted successfully!');
                navigate('/my-applications');
            }
        } catch (error) {
            console.error('Failed to apply:', error);
            toast.error('Failed to submit application');
        } finally {
            setApplying(false);
        }
    };

    if (loading) return <Loader />;
    if (!job) return <div>Job not found</div>;

    return (
        <div className="job-details-container">
            <button onClick={() => navigate(-1)} className="back-button">
                <i className="fas fa-arrow-left"></i> Back to Jobs
            </button>

            <div className="job-details-card">
                <div className="job-header">
                    <h1>{job.title}</h1>
                    <span className="company-name">{job.company_name}</span>
                </div>

                <div className="job-meta-grid">
                    <div className="meta-item">
                        <i className="fas fa-dollar-sign"></i>
                        <div>
                            <label>Hourly Rate</label>
                            <span>${job.pay_per_hour}/hr</span>
                        </div>
                    </div>
                    <div className="meta-item">
                        <i className="fas fa-briefcase"></i>
                        <div>
                            <label>Experience Level</label>
                            <span>{job.experience_level}</span>
                        </div>
                    </div>
                    <div className="meta-item">
                        <i className="fas fa-clock"></i>
                        <div>
                            <label>Job Type</label>
                            <span>{job.job_type}</span>
                        </div>
                    </div>
                    <div className="meta-item">
                        <i className="fas fa-map-marker-alt"></i>
                        <div>
                            <label>Location</label>
                            <span>{job.is_remote ? 'Remote' : job.location || 'Not specified'}</span>
                        </div>
                    </div>
                </div>

                <div className="job-section">
                    <h3>Description</h3>
                    <p>{job.description}</p>
                </div>

                {job.requirements && (
                    <div className="job-section">
                        <h3>Requirements</h3>
                        <p>{job.requirements}</p>
                    </div>
                )}

                {job.responsibilities && (
                    <div className="job-section">
                        <h3>Responsibilities</h3>
                        <p>{job.responsibilities}</p>
                    </div>
                )}

                {job.required_skills?.length > 0 && (
                    <div className="job-section">
                        <h3>Required Skills</h3>
                        <div className="skills-list">
                            {job.required_skills.map((skill, index) => (
                                <span key={index} className="skill-badge">{skill}</span>
                            ))}
                        </div>
                    </div>
                )}

                {job.tech_stack?.length > 0 && (
                    <div className="job-section">
                        <h3>Tech Stack</h3>
                        <div className="tech-stack-list">
                            {job.tech_stack.map((tech, index) => (
                                <span key={index} className="tech-badge">{tech}</span>
                            ))}
                        </div>
                    </div>
                )}

                {!showApplicationForm ? (
                    <button
                        onClick={() => setShowApplicationForm(true)}
                        className="btn btn-primary btn-large"
                    >
                        I'm Interested
                    </button>
                ) : (
                    <form onSubmit={handleApply} className="application-form">
                        <h3>Submit Your Application</h3>

                        <div className="form-group">
                            <label>Cover Letter</label>
                            <textarea
                                value={application.cover_letter}
                                onChange={(e) => setApplication({ ...application, cover_letter: e.target.value })}
                                placeholder="Introduce yourself and explain why you're a good fit for this role..."
                                rows="5"
                                required
                            />
                        </div>

                        <div className="form-row">
                            <div className="form-group">
                                <label>Proposed Rate ($/hr)</label>
                                <input
                                    type="number"
                                    value={application.proposed_rate}
                                    onChange={(e) => setApplication({ ...application, proposed_rate: e.target.value })}
                                    placeholder="e.g., 50"
                                    min="0"
                                    step="0.01"
                                />
                            </div>

                            <div className="form-group">
                                <label>Availability Date</label>
                                <input
                                    type="date"
                                    value={application.availability_date}
                                    onChange={(e) => setApplication({ ...application, availability_date: e.target.value })}
                                    min={new Date().toISOString().split('T')[0]}
                                />
                            </div>
                        </div>

                        <div className="form-actions">
                            <button type="submit" className="btn btn-primary" disabled={applying}>
                                {applying ? 'Submitting...' : 'Submit Application'}
                            </button>
                            <button
                                type="button"
                                className="btn btn-outline"
                                onClick={() => setShowApplicationForm(false)}
                            >
                                Cancel
                            </button>
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
};

export default JobDetails;