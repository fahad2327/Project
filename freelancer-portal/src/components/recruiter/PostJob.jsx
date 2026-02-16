import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import recruiterService from '../../services/recruiterService';
import toast from 'react-hot-toast';
import './Recruiter.css';

const PostJob = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [jobData, setJobData] = useState({
        title: '',
        description: '',
        requirements: '',
        responsibilities: '',
        pay_per_hour: '',
        experience_level: 'junior',
        job_type: 'freelance',
        location: '',
        is_remote: true,
        required_skills: [],
        tech_stack: [],
        benefits: '',
        application_deadline: ''
    });

    const [skillInput, setSkillInput] = useState('');
    const [techInput, setTechInput] = useState('');
    const [errors, setErrors] = useState({});

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setJobData({
            ...jobData,
            [name]: type === 'checkbox' ? checked : value
        });
        // Clear error for this field
        if (errors[name]) {
            setErrors({ ...errors, [name]: null });
        }
    };

    const handleAddSkill = () => {
        if (skillInput.trim() && !jobData.required_skills.includes(skillInput.trim())) {
            setJobData({
                ...jobData,
                required_skills: [...jobData.required_skills, skillInput.trim()]
            });
            setSkillInput('');
        }
    };

    const handleRemoveSkill = (skill) => {
        setJobData({
            ...jobData,
            required_skills: jobData.required_skills.filter(s => s !== skill)
        });
    };

    const handleAddTech = () => {
        if (techInput.trim() && !jobData.tech_stack.includes(techInput.trim())) {
            setJobData({
                ...jobData,
                tech_stack: [...jobData.tech_stack, techInput.trim()]
            });
            setTechInput('');
        }
    };

    const handleRemoveTech = (tech) => {
        setJobData({
            ...jobData,
            tech_stack: jobData.tech_stack.filter(t => t !== tech)
        });
    };

    const validateForm = () => {
        const newErrors = {};

        if (!jobData.title.trim()) {
            newErrors.title = 'Job title is required';
        }

        if (!jobData.description.trim()) {
            newErrors.description = 'Job description is required';
        }

        if (!jobData.pay_per_hour) {
            newErrors.pay_per_hour = 'Pay per hour is required';
        } else if (jobData.pay_per_hour <= 0) {
            newErrors.pay_per_hour = 'Pay per hour must be greater than 0';
        }

        if (!jobData.experience_level) {
            newErrors.experience_level = 'Experience level is required';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!validateForm()) {
            toast.error('Please fix the errors in the form');
            return;
        }

        setLoading(true);

        try {
            const response = await recruiterService.createJob(jobData);
            if (response.success) {
                toast.success('Job posted successfully!');
                navigate('/manage-jobs');
            } else {
                toast.error(response.message || 'Failed to post job');
            }
        } catch (error) {
            console.error('Failed to post job:', error);
            toast.error('Failed to post job');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="post-job-container">
            <div className="post-job-header">
                <h1>Post a New Job</h1>
                <p>Fill in the details below to attract the best freelancers</p>
            </div>

            <form onSubmit={handleSubmit} className="post-job-form">
                {/* Basic Information */}
                <div className="form-section">
                    <h2>Basic Information</h2>

                    <div className="form-group">
                        <label htmlFor="title">Job Title *</label>
                        <input
                            type="text"
                            id="title"
                            name="title"
                            value={jobData.title}
                            onChange={handleChange}
                            className={errors.title ? 'error' : ''}
                            placeholder="e.g., Senior React Developer"
                        />
                        {errors.title && <span className="error-message">{errors.title}</span>}
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label htmlFor="pay_per_hour">Pay Per Hour ($) *</label>
                            <input
                                type="number"
                                id="pay_per_hour"
                                name="pay_per_hour"
                                value={jobData.pay_per_hour}
                                onChange={handleChange}
                                className={errors.pay_per_hour ? 'error' : ''}
                                placeholder="e.g., 50"
                                min="0"
                                step="0.01"
                            />
                            {errors.pay_per_hour && <span className="error-message">{errors.pay_per_hour}</span>}
                        </div>

                        <div className="form-group">
                            <label htmlFor="experience_level">Experience Level *</label>
                            <select
                                id="experience_level"
                                name="experience_level"
                                value={jobData.experience_level}
                                onChange={handleChange}
                                className={errors.experience_level ? 'error' : ''}
                            >
                                <option value="junior">Junior (0-2 years)</option>
                                <option value="mid">Mid-Level (3-5 years)</option>
                                <option value="senior">Senior (5+ years)</option>
                            </select>
                            {errors.experience_level && <span className="error-message">{errors.experience_level}</span>}
                        </div>
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label htmlFor="job_type">Job Type</label>
                            <select
                                id="job_type"
                                name="job_type"
                                value={jobData.job_type}
                                onChange={handleChange}
                            >
                                <option value="freelance">Freelance</option>
                                <option value="full-time">Full Time</option>
                                <option value="part-time">Part Time</option>
                                <option value="contract">Contract</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label htmlFor="location">Location</label>
                            <input
                                type="text"
                                id="location"
                                name="location"
                                value={jobData.location}
                                onChange={handleChange}
                                placeholder="e.g., Remote, New York, London"
                            />
                        </div>
                    </div>

                    <div className="form-group checkbox">
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                name="is_remote"
                                checked={jobData.is_remote}
                                onChange={handleChange}
                            />
                            <span>This is a remote position</span>
                        </label>
                    </div>
                </div>

                {/* Job Description */}
                <div className="form-section">
                    <h2>Job Description</h2>

                    <div className="form-group">
                        <label htmlFor="description">Description *</label>
                        <textarea
                            id="description"
                            name="description"
                            rows="6"
                            value={jobData.description}
                            onChange={handleChange}
                            className={errors.description ? 'error' : ''}
                            placeholder="Describe the role, responsibilities, and what makes this opportunity great..."
                        />
                        {errors.description && <span className="error-message">{errors.description}</span>}
                    </div>

                    <div className="form-group">
                        <label htmlFor="requirements">Requirements</label>
                        <textarea
                            id="requirements"
                            name="requirements"
                            rows="4"
                            value={jobData.requirements}
                            onChange={handleChange}
                            placeholder="List the required skills, qualifications, and experience..."
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="responsibilities">Responsibilities</label>
                        <textarea
                            id="responsibilities"
                            name="responsibilities"
                            rows="4"
                            value={jobData.responsibilities}
                            onChange={handleChange}
                            placeholder="Describe the day-to-day responsibilities and tasks..."
                        />
                    </div>
                </div>

                {/* Skills & Tech Stack */}
                <div className="form-section">
                    <h2>Skills & Technologies</h2>

                    <div className="form-group">
                        <label>Required Skills</label>
                        <div className="input-with-button">
                            <input
                                type="text"
                                value={skillInput}
                                onChange={(e) => setSkillInput(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddSkill())}
                                placeholder="e.g., React, Python, UI Design"
                            />
                            <button
                                type="button"
                                onClick={handleAddSkill}
                                className="btn btn-outline"
                            >
                                Add
                            </button>
                        </div>
                    </div>

                    <div className="skills-container">
                        {jobData.required_skills.map((skill, index) => (
                            <span key={index} className="skill-tag">
                                {skill}
                                <button
                                    type="button"
                                    onClick={() => handleRemoveSkill(skill)}
                                    className="remove-tag"
                                >
                                    ×
                                </button>
                            </span>
                        ))}
                    </div>

                    <div className="form-group">
                        <label>Tech Stack</label>
                        <div className="input-with-button">
                            <input
                                type="text"
                                value={techInput}
                                onChange={(e) => setTechInput(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddTech())}
                                placeholder="e.g., AWS, Docker, MongoDB"
                            />
                            <button
                                type="button"
                                onClick={handleAddTech}
                                className="btn btn-outline"
                            >
                                Add
                            </button>
                        </div>
                    </div>

                    <div className="tech-stack-container">
                        {jobData.tech_stack.map((tech, index) => (
                            <span key={index} className="tech-tag">
                                {tech}
                                <button
                                    type="button"
                                    onClick={() => handleRemoveTech(tech)}
                                    className="remove-tag"
                                >
                                    ×
                                </button>
                            </span>
                        ))}
                    </div>
                </div>

                {/* Additional Information */}
                <div className="form-section">
                    <h2>Additional Information</h2>

                    <div className="form-group">
                        <label htmlFor="benefits">Benefits</label>
                        <textarea
                            id="benefits"
                            name="benefits"
                            rows="3"
                            value={jobData.benefits}
                            onChange={handleChange}
                            placeholder="List the benefits and perks (e.g., flexible hours, health insurance, etc.)"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="application_deadline">Application Deadline</label>
                        <input
                            type="date"
                            id="application_deadline"
                            name="application_deadline"
                            value={jobData.application_deadline}
                            onChange={handleChange}
                            min={new Date().toISOString().split('T')[0]}
                        />
                    </div>
                </div>

                {/* Form Actions */}
                <div className="form-actions">
                    <button
                        type="submit"
                        className="btn btn-primary btn-large"
                        disabled={loading}
                    >
                        {loading ? (
                            <>
                                <span className="spinner"></span>
                                Posting Job...
                            </>
                        ) : (
                            <>
                                <i className="fas fa-bullhorn"></i>
                                Post Job
                            </>
                        )}
                    </button>
                    <button
                        type="button"
                        className="btn btn-outline btn-large"
                        onClick={() => navigate('/dashboard')}
                    >
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    );
};

export default PostJob;