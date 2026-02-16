import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import recruiterService from '../../services/recruiterService';
import toast from 'react-hot-toast';
import Loader from '../common/Loader';
import './Recruiter.css';

const RecruiterProfile = () => {
    const { user } = useAuth();
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [profile, setProfile] = useState({
        company_name: '',
        company_website: '',
        company_size: '',
        industry: '',
        company_description: '',
        location: '',
        phone: ''
    });

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            const response = await recruiterService.getProfile();
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
        const { name, value } = e.target;
        setProfile({ ...profile, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);
        try {
            const response = await recruiterService.updateProfile(profile);
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
            <h1>Company Profile</h1>

            <form onSubmit={handleSubmit} className="profile-form">
                <div className="form-section">
                    <h2>Company Information</h2>

                    <div className="form-group">
                        <label>Company Name</label>
                        <input
                            type="text"
                            name="company_name"
                            value={profile.company_name || ''}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Company Website</label>
                        <input
                            type="url"
                            name="company_website"
                            value={profile.company_website || ''}
                            onChange={handleChange}
                            placeholder="https://example.com"
                        />
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Company Size</label>
                            <select
                                name="company_size"
                                value={profile.company_size || ''}
                                onChange={handleChange}
                            >
                                <option value="">Select size</option>
                                <option value="1-10">1-10 employees</option>
                                <option value="11-50">11-50 employees</option>
                                <option value="51-200">51-200 employees</option>
                                <option value="201-500">201-500 employees</option>
                                <option value="500+">500+ employees</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Industry</label>
                            <input
                                type="text"
                                name="industry"
                                value={profile.industry || ''}
                                onChange={handleChange}
                                placeholder="e.g., Technology, Healthcare"
                            />
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Company Description</label>
                        <textarea
                            name="company_description"
                            value={profile.company_description || ''}
                            onChange={handleChange}
                            rows="5"
                            placeholder="Tell freelancers about your company..."
                        />
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Location</label>
                            <input
                                type="text"
                                name="location"
                                value={profile.location || ''}
                                onChange={handleChange}
                                placeholder="City, Country"
                            />
                        </div>

                        <div className="form-group">
                            <label>Phone</label>
                            <input
                                type="tel"
                                name="phone"
                                value={profile.phone || ''}
                                onChange={handleChange}
                                placeholder="+1 234 567 8900"
                            />
                        </div>
                    </div>
                </div>

                <div className="form-actions">
                    <button type="submit" className="btn btn-primary" disabled={saving}>
                        {saving ? 'Saving...' : 'Save Profile'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default RecruiterProfile;