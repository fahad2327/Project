import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import freelancerService from '../../services/freelancerService';
import Loader from '../common/Loader';
import toast from 'react-hot-toast';
import './Freelancer.css';

const JobSearch = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filters, setFilters] = useState({
        search: '',
        experience_level: '',
        min_pay: '',
        max_pay: '',
        job_type: '',
        is_remote: ''
    });
    const [showFilters, setShowFilters] = useState(false);

    useEffect(() => {
        searchJobs();
    }, []);

    const searchJobs = async () => {
        setLoading(true);
        try {
            // Create a copy of filters and remove empty values
            const activeFilters = {};

            // Only add filters that have actual values
            Object.keys(filters).forEach(key => {
                const value = filters[key];
                if (value !== '' && value !== null && value !== undefined) {
                    // Special handling for min_pay and max_pay - only add if they are valid numbers
                    if (key === 'min_pay' || key === 'max_pay') {
                        if (value && !isNaN(value) && parseFloat(value) > 0) {
                            activeFilters[key] = value;
                        }
                    } else {
                        activeFilters[key] = value;
                    }
                }
            });

            console.log('Searching with filters:', activeFilters); // Debug log

            const response = await freelancerService.searchJobs(activeFilters);
            console.log('Search response:', response); // Debug log

            if (response.success) {
                setJobs(response.jobs);
                if (response.jobs.length === 0) {
                    console.log('No jobs found with these filters');
                }
            }
        } catch (error) {
            console.error('Failed to search jobs:', error);
            toast.error('Failed to search jobs');
        } finally {
            setLoading(false);
        }
    };

    const handleFilterChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFilters({
            ...filters,
            [name]: type === 'checkbox' ? checked : value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        searchJobs();
    };

    const clearFilters = () => {
        setFilters({
            search: '',
            experience_level: '',
            min_pay: '',
            max_pay: '',
            job_type: '',
            is_remote: ''
        });
        setTimeout(() => searchJobs(), 0);
    };

    const experienceLevels = ['junior', 'mid', 'senior'];
    const jobTypes = ['full-time', 'part-time', 'contract', 'freelance'];

    return (
        <div className="job-search-container">
            <div className="job-search-header">
                <h1>Find Your Next Opportunity</h1>
                <p>Browse through thousands of jobs from top companies</p>
            </div>

            {/* Search Bar */}
            <div className="search-bar-container">
                <form onSubmit={handleSubmit} className="search-form">
                    <div className="search-input-wrapper">
                        <i className="fas fa-search"></i>
                        <input
                            type="text"
                            name="search"
                            value={filters.search}
                            onChange={handleFilterChange}
                            placeholder="Search by job title, skills, or keywords..."
                        />
                    </div>
                    <button type="submit" className="btn btn-primary">
                        Search Jobs
                    </button>
                    <button
                        type="button"
                        className="btn btn-outline"
                        onClick={() => setShowFilters(!showFilters)}
                    >
                        <i className={`fas fa-${showFilters ? 'times' : 'filter'}`}></i>
                        {showFilters ? 'Hide Filters' : 'Filters'}
                    </button>
                </form>
            </div>

            {/* Filters */}
            {showFilters && (
                <div className="filters-panel">
                    <div className="filters-header">
                        <h3>Filter Jobs</h3>
                        <button type="button" onClick={clearFilters} className="clear-filters">
                            Clear All
                        </button>
                    </div>

                    <div className="filters-grid">
                        <div className="filter-group">
                            <label>Experience Level</label>
                            <select
                                name="experience_level"
                                value={filters.experience_level}
                                onChange={handleFilterChange}
                            >
                                <option value="">All Levels</option>
                                {experienceLevels.map(level => (
                                    <option key={level} value={level}>
                                        {level.charAt(0).toUpperCase() + level.slice(1)}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="filter-group">
                            <label>Job Type</label>
                            <select
                                name="job_type"
                                value={filters.job_type}
                                onChange={handleFilterChange}
                            >
                                <option value="">All Types</option>
                                {jobTypes.map(type => (
                                    <option key={type} value={type}>
                                        {type.charAt(0).toUpperCase() + type.slice(1)}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="filter-group">
                            <label>Minimum Pay ($/hr)</label>
                            <input
                                type="number"
                                name="min_pay"
                                value={filters.min_pay}
                                onChange={handleFilterChange}
                                placeholder="e.g., 30"
                                min="0"
                            />
                        </div>

                        <div className="filter-group">
                            <label>Maximum Pay ($/hr)</label>
                            <input
                                type="number"
                                name="max_pay"
                                value={filters.max_pay}
                                onChange={handleFilterChange}
                                placeholder="e.g., 100"
                                min="0"
                            />
                        </div>

                        <div className="filter-group checkbox">
                            <label className="checkbox-label">
                                <input
                                    type="checkbox"
                                    name="is_remote"
                                    checked={filters.is_remote}
                                    onChange={handleFilterChange}
                                />
                                <span>Remote Only</span>
                            </label>
                        </div>
                    </div>

                    <div className="filters-actions">
                        <button onClick={searchJobs} className="btn btn-primary">
                            Apply Filters
                        </button>
                    </div>
                </div>
            )}

            {/* Results */}
            <div className="jobs-results">
                <div className="results-header">
                    <h3>{jobs.length} Jobs Found</h3>
                    <select className="sort-select">
                        <option>Most Recent</option>
                        <option>Pay: High to Low</option>
                        <option>Pay: Low to High</option>
                    </select>
                </div>

                {loading ? (
                    <Loader />
                ) : jobs.length > 0 ? (
                    <div className="jobs-grid">
                        {jobs.map(job => (
                            <div key={job.id} className="job-card">
                                <div className="job-card-header">
                                    <h3 className="job-title">{job.title}</h3>
                                    <span className="company-name">{job.company_name}</span>
                                </div>

                                <div className="job-details">
                                    <div className="job-detail">
                                        <i className="fas fa-dollar-sign"></i>
                                        <span>${job.pay_per_hour}/hr</span>
                                    </div>
                                    <div className="job-detail">
                                        <i className="fas fa-briefcase"></i>
                                        <span>{job.experience_level}</span>
                                    </div>
                                    <div className="job-detail">
                                        <i className="fas fa-clock"></i>
                                        <span>{job.job_type}</span>
                                    </div>
                                    {job.is_remote && (
                                        <div className="job-detail remote">
                                            <i className="fas fa-globe"></i>
                                            <span>Remote</span>
                                        </div>
                                    )}
                                </div>

                                <p className="job-description">
                                    {job.description?.substring(0, 150)}...
                                </p>

                                {job.required_skills && job.required_skills.length > 0 && (
                                    <div className="job-skills">
                                        {job.required_skills.slice(0, 4).map(skill => (
                                            <span key={skill} className="skill-badge">{skill}</span>
                                        ))}
                                        {job.required_skills.length > 4 && (
                                            <span className="skill-badge more">+{job.required_skills.length - 4}</span>
                                        )}
                                    </div>
                                )}

                                <div className="job-card-footer">
                                    <span className="posted-date">
                                        Posted {new Date(job.created_at).toLocaleDateString()}
                                    </span>
                                    <Link to={`/jobs/${job.id}`} className="btn btn-primary btn-small">
                                        View Details
                                    </Link>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="no-results">
                        <i className="fas fa-search"></i>
                        <h3>No jobs found</h3>
                        <p>Try adjusting your search filters or check back later</p>
                        <button onClick={clearFilters} className="btn btn-outline">
                            Clear All Filters
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default JobSearch;