import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import freelancerService from '../../services/freelancerService';
import toast from 'react-hot-toast';
import Loader from '../common/Loader';
import './Freelancer.css';

const FreelancerProfile = () => {
    const { user } = useAuth();
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [profile, setProfile] = useState({
        bio: '',
        hourly_rate: '',
        education: '',
        experience: '',
        years_of_experience: '',
        github_url: '',
        linkedin_url: '',
        portfolio_url: '',
        skills: [],
        tech_stacks: [],
        is_available: true
    });

    const [skillInput, setSkillInput] = useState('');
    const [techInput, setTechInput] = useState('');
    const [showSkillSuggestions, setShowSkillSuggestions] = useState(false);
    const [showTechSuggestions, setShowTechSuggestions] = useState(false);
    const [skillSuggestions, setSkillSuggestions] = useState([]);
    const [techSuggestions, setTechSuggestions] = useState([]);

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            const response = await freelancerService.getProfile();
            if (response.success) {
                setProfile(response.profile);
            }
        } catch (error) {
            console.error('Failed to fetch profile:', error);
            toast.error('Failed to load profile');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setProfile({
            ...profile,
            [name]: type === 'checkbox' ? checked : value
        });
    };

    const handleAddSkill = () => {
        if (skillInput.trim() && !profile.skills.some(s => s.name.toLowerCase() === skillInput.toLowerCase())) {
            setProfile({
                ...profile,
                skills: [...profile.skills, { name: skillInput.trim(), proficiency_level: 'intermediate' }]
            });
            setSkillInput('');
        }
    };

    const handleRemoveSkill = (skillName) => {
        setProfile({
            ...profile,
            skills: profile.skills.filter(s => s.name !== skillName)
        });
    };

    const handleAddTech = () => {
        if (techInput.trim() && !profile.tech_stacks.some(t => t.name.toLowerCase() === techInput.toLowerCase())) {
            setProfile({
                ...profile,
                tech_stacks: [...profile.tech_stacks, { name: techInput.trim(), experience_years: 0 }]
            });
            setTechInput('');
        }
    };

    const handleRemoveTech = (techName) => {
        setProfile({
            ...profile,
            tech_stacks: profile.tech_stacks.filter(t => t.name !== techName)
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);

        try {
            const response = await freelancerService.updateProfile(profile);
            if (response.success) {
                toast.success('Profile updated successfully!');
            }
        } catch (error) {
            console.error('Failed to update profile:', error);
            toast.error('Failed to update profile');
        } finally {
            setSaving(false);
        }
    };

    if (loading) return <Loader />;

    return (
        <div className="profile-container">
            <div className="profile-header">
                <h1>Freelancer Profile</h1>
                <p>Complete your profile to attract more opportunities</p>
            </div>

            <form onSubmit={handleSubmit} className="profile-form">
                {/* Personal Information */}
                <div className="form-section">
                    <h2>Personal Information</h2>
                    <div className="form-row">
                        <div className="form-group">
                            <label>First Name</label>
                            <input
                                type="text"
                                value={user?.first_name || ''}
                                disabled
                                className="disabled"
                            />
                        </div>
                        <div className="form-group">
                            <label>Last Name</label>
                            <input
                                type="text"
                                value={user?.last_name || ''}
                                disabled
                                className="disabled"
                            />
                        </div>
                    </div>
                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            value={user?.email || ''}
                            disabled
                            className="disabled"
                        />
                    </div>
                </div>

                {/* Professional Information */}
                <div className="form-section">
                    <h2>Professional Information</h2>

                    <div className="form-group">
                        <label htmlFor="bio">Bio</label>
                        <textarea
                            id="bio"
                            name="bio"
                            rows="4"
                            value={profile.bio || ''}
                            onChange={handleChange}
                            placeholder="Tell recruiters about yourself, your experience, and what you're looking for..."
                        />
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label htmlFor="hourly_rate">Hourly Rate ($)</label>
                            <input
                                type="number"
                                id="hourly_rate"
                                name="hourly_rate"
                                value={profile.hourly_rate || ''}
                                onChange={handleChange}
                                placeholder="e.g., 50"
                                min="0"
                                step="0.01"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="years_of_experience">Years of Experience</label>
                            <input
                                type="number"
                                id="years_of_experience"
                                name="years_of_experience"
                                value={profile.years_of_experience || ''}
                                onChange={handleChange}
                                placeholder="e.g., 5"
                                min="0"
                            />
                        </div>
                    </div>

                    <div className="form-group">
                        <label htmlFor="education">Education</label>
                        <textarea
                            id="education"
                            name="education"
                            rows="3"
                            value={profile.education || ''}
                            onChange={handleChange}
                            placeholder="e.g., B.Tech Computer Science, XYZ University, 2020"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="experience">Work Experience</label>
                        <textarea
                            id="experience"
                            name="experience"
                            rows="4"
                            value={profile.experience || ''}
                            onChange={handleChange}
                            placeholder="Describe your previous work experience, projects, and achievements..."
                        />
                    </div>
                </div>

                {/* Skills Section */}
                <div className="form-section">
                    <h2>Skills & Expertise</h2>

                    <div className="skills-input-group">
                        <div className="form-group">
                            <label>Add Skills</label>
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
                    </div>

                    <div className="skills-container">
                        {profile.skills?.map((skill) => (
                            <span key={skill.id || skill.name} className="skill-tag">
                                {skill.name}
                                <button
                                    type="button"
                                    onClick={() => handleRemoveSkill(skill.name)}
                                    className="remove-tag"
                                >
                                    ×
                                </button>
                            </span>
                        ))}
                    </div>
                </div>

                {/* Tech Stack Section */}
                <div className="form-section">
                    <h2>Tech Stack</h2>

                    <div className="skills-input-group">
                        <div className="form-group">
                            <label>Add Technologies</label>
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
                    </div>

                    <div className="tech-stack-container">
                        {profile.tech_stacks?.map((tech) => (
                            <span key={tech.id || tech.name} className="tech-tag">
                                {tech.name}
                                <button
                                    type="button"
                                    onClick={() => handleRemoveTech(tech.name)}
                                    className="remove-tag"
                                >
                                    ×
                                </button>
                            </span>
                        ))}
                    </div>
                </div>

                {/* Social Links */}
                <div className="form-section">
                    <h2>Social Links</h2>

                    <div className="form-group">
                        <label htmlFor="github_url">GitHub URL</label>
                        <input
                            type="url"
                            id="github_url"
                            name="github_url"
                            value={profile.github_url || ''}
                            onChange={handleChange}
                            placeholder="https://github.com/username"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="linkedin_url">LinkedIn URL</label>
                        <input
                            type="url"
                            id="linkedin_url"
                            name="linkedin_url"
                            value={profile.linkedin_url || ''}
                            onChange={handleChange}
                            placeholder="https://linkedin.com/in/username"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="portfolio_url">Portfolio URL</label>
                        <input
                            type="url"
                            id="portfolio_url"
                            name="portfolio_url"
                            value={profile.portfolio_url || ''}
                            onChange={handleChange}
                            placeholder="https://yourportfolio.com"
                        />
                    </div>
                </div>

                {/* Availability */}
                <div className="form-section">
                    <h2>Availability</h2>

                    <label className="checkbox-label">
                        <input
                            type="checkbox"
                            name="is_available"
                            checked={profile.is_available}
                            onChange={handleChange}
                        />
                        <span>Available for work</span>
                    </label>
                </div>

                {/* Form Actions */}
                <div className="form-actions">
                    <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={saving}
                    >
                        {saving ? (
                            <>
                                <span className="spinner"></span>
                                Saving...
                            </>
                        ) : (
                            'Save Profile'
                        )}
                    </button>
                    <button
                        type="button"
                        className="btn btn-outline"
                        onClick={() => window.history.back()}
                    >
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    );
};

export default FreelancerProfile;