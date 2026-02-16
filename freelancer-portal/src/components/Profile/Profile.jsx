import React, { useState, useEffect } from 'react';
import authService from '../../services/authService';
import './Profile.css';

const Profile = ({ user, onUpdateUser }) => {
    const [profile, setProfile] = useState({
        name: user?.name || '',
        email: user?.email || '',
        phone: '',
        address: '',
        skills: '',
        bio: ''
    });
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState({ type: '', text: '' });

    useEffect(() => {
        fetchUserProfile();
    }, []);

    const fetchUserProfile = async () => {
        try {
            const data = await authService.getUserProfile();
            if (data.success) {
                setProfile({
                    name: data.user.name,
                    email: data.user.email,
                    phone: data.user.phone || '',
                    address: data.user.address || '',
                    skills: data.user.skills || '',
                    bio: data.user.bio || ''
                });
            }
        } catch (error) {
            console.error('Error fetching profile:', error);
        }
    };

    const handleChange = (e) => {
        setProfile({
            ...profile,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage({ type: '', text: '' });

        try {
            const data = await authService.updateProfile({
                name: profile.name,
                phone: profile.phone,
                address: profile.address,
                skills: profile.skills,
                bio: profile.bio
            });

            if (data.success) {
                setMessage({ type: 'success', text: 'Profile updated successfully!' });
                onUpdateUser({ ...user, name: profile.name });
            } else {
                setMessage({ type: 'error', text: data.message || 'Failed to update profile' });
            }
        } catch (error) {
            setMessage({ type: 'error', text: 'Failed to connect to server' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="profile-container">
            <div className="profile-card">
                <div className="profile-header">
                    <h2>Profile Settings</h2>
                    <p>Manage your account information</p>
                </div>

                {message.text && (
                    <div className={`profile-message ${message.type}`}>
                        {message.text}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="profile-form">
                    <div className="form-section">
                        <h3>Personal Information</h3>

                        <div className="form-group">
                            <label htmlFor="name">Full Name</label>
                            <input
                                type="text"
                                id="name"
                                name="name"
                                value={profile.name}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="email">Email Address</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={profile.email}
                                disabled
                                className="disabled"
                            />
                            <small>Email cannot be changed</small>
                        </div>

                        <div className="form-group">
                            <label htmlFor="phone">Phone Number</label>
                            <input
                                type="tel"
                                id="phone"
                                name="phone"
                                value={profile.phone}
                                onChange={handleChange}
                                placeholder="Enter your phone number"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="address">Address</label>
                            <input
                                type="text"
                                id="address"
                                name="address"
                                value={profile.address}
                                onChange={handleChange}
                                placeholder="Enter your address"
                            />
                        </div>
                    </div>

                    <div className="form-section">
                        <h3>Professional Information</h3>

                        <div className="form-group">
                            <label htmlFor="skills">Skills</label>
                            <input
                                type="text"
                                id="skills"
                                name="skills"
                                value={profile.skills}
                                onChange={handleChange}
                                placeholder="e.g., React, Python, UI Design"
                            />
                            <small>Separate skills with commas</small>
                        </div>

                        <div className="form-group">
                            <label htmlFor="bio">Bio</label>
                            <textarea
                                id="bio"
                                name="bio"
                                rows="4"
                                value={profile.bio}
                                onChange={handleChange}
                                placeholder="Tell us about yourself"
                            ></textarea>
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="profile-button"
                        disabled={loading}
                    >
                        {loading ? 'Updating...' : 'Update Profile'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Profile;