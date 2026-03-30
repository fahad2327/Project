// import React, { useState, useEffect } from 'react';
// import { Link } from 'react-router-dom';
// import recruiterService from '../../services/recruiterService';
// import Loader from '../common/Loader';
// import './Recruiter.css';

// const ManageJobs = () => {
//     const [jobs, setJobs] = useState([]);
//     const [loading, setLoading] = useState(true);

//     useEffect(() => {
//         fetchJobs();
//     }, []);

//     const fetchJobs = async () => {
//         try {
//             const response = await recruiterService.getMyJobs();
//             if (response.success) {
//                 setJobs(response.jobs);
//             }
//         } catch (error) {
//             console.error('Failed to fetch jobs:', error);
//         } finally {
//             setLoading(false);
//         }
//     };

//     if (loading) return <Loader />;

//     return (
//         <div className="manage-jobs-container">
//             <div className="header">
//                 <h1>Manage Jobs</h1>
//                 <Link to="/post-job" className="btn btn-primary">
//                     <i className="fas fa-plus"></i> Post New Job
//                 </Link>
//             </div>

//             {jobs.length === 0 ? (
//                 <div className="empty-state">
//                     <i className="fas fa-briefcase"></i>
//                     <h3>No jobs posted yet</h3>
//                     <p>Post your first job and start receiving applications</p>
//                     <Link to="/post-job" className="btn btn-primary">
//                         Post a Job
//                     </Link>
//                 </div>
//             ) : (
//                 <div className="jobs-table">
//                     <table>
//                         <thead>
//                             <tr>
//                                 <th>Job Title</th>
//                                 <th>Applications</th>
//                                 <th>Posted Date</th>
//                                 <th>Status</th>
//                                 <th>Actions</th>
//                             </tr>
//                         </thead>
//                         <tbody>
//                             {jobs.map((job) => (
//                                 <tr key={job.id}>
//                                     <td>
//                                         <strong>{job.title}</strong>
//                                         <div className="job-meta">
//                                             <span>${job.pay_per_hour}/hr</span>
//                                             <span>{job.experience_level}</span>
//                                         </div>
//                                     </td>
//                                     <td>
//                                         <span className="applications-count">
//                                             {job.applications_count || 0}
//                                         </span>
//                                     </td>
//                                     <td>{new Date(job.created_at).toLocaleDateString()}</td>
//                                     <td>
//                                         <span className={`status-badge ${job.is_active ? 'active' : 'inactive'}`}>
//                                             {job.is_active ? 'Active' : 'Closed'}
//                                         </span>
//                                     </td>
//                                     <td>
//                                         <div className="action-buttons">
//                                             <Link
//                                                 to={`/jobs/${job.id}/applications`}
//                                                 className="btn btn-outline btn-small"
//                                             >
//                                                 View Applications
//                                             </Link>
//                                             <button className="btn btn-outline btn-small">
//                                                 <i className="fas fa-edit"></i>
//                                             </button>
//                                         </div>
//                                     </td>
//                                 </tr>
//                             ))}
//                         </tbody>
//                     </table>
//                 </div>
//             )}
//         </div>
//     );
// };

// export default ManageJobs;
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import recruiterService from '../../services/recruiterService';
import Loader from '../common/Loader';
import toast from 'react-hot-toast';
import './Recruiter.css';

const ManageJobs = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchJobs();
    }, []);

    const handleDeleteJob = async (jobId) => {
        if (window.confirm('Are you sure you want to delete this job? This action cannot be undone.')) {
            try {
                const response = await recruiterService.deleteJob(jobId);
                if (response.success) {
                    toast.success('Job deleted successfully');
                    fetchJobs(); // refresh the list
                } else {
                    toast.error(response.message || 'Failed to delete job');
                }
            } catch (error) {
                toast.error('Error deleting job');
            }
        }
    };

    const fetchJobs = async () => {
        try {
            const response = await recruiterService.getMyJobs();
            if (response.success) {
                setJobs(response.jobs);
            }
        } catch (error) {
            console.error('Failed to fetch jobs:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <Loader />;

    return (
        <div className="manage-jobs-container">
            <div className="header">
                <h1>Manage Jobs</h1>
                <Link to="/post-job" className="btn btn-primary">
                    <i className="fas fa-plus"></i> Post New Job
                </Link>
            </div>

            {jobs.length === 0 ? (
                <div className="empty-state">
                    <i className="fas fa-briefcase"></i>
                    <h3>No jobs posted yet</h3>
                    <p>Post your first job and start receiving applications</p>
                    <Link to="/post-job" className="btn btn-primary">Post a Job</Link>
                </div>
            ) : (
                <div className="jobs-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Job Title</th>
                                <th>Applications</th>
                                <th>Posted Date</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {jobs.map((job) => (
                                <tr key={job.id}>
                                    <td>
                                        <strong>{job.title}</strong>
                                        <div className="job-meta">
                                            <span>${job.pay_per_hour}/hr</span>
                                            <span>{job.experience_level}</span>
                                        </div>
                                    </td>
                                    <td><span className="applications-count">{job.applications_count || 0}</span></td>
                                    <td>{new Date(job.created_at).toLocaleDateString()}</td>
                                    <td>
                                        <span className={`status-badge ${job.is_active ? 'active' : 'inactive'}`}>
                                            {job.is_active ? 'Active' : 'Closed'}
                                        </span>
                                    </td>
                                    <td>
                                        {/* <div className="action-buttons">
                                            <Link to={`/recruiter/jobs/${job.id}/applications`} className="btn btn-outline btn-small">
                                                View Applications
                                            </Link>
                                            <button className="btn btn-outline btn-small"><i className="fas fa-edit"></i></button>
                                        </div> */}
                                        <div className="action-buttons">
                                            <Link to={`/recruiter/jobs/${job.id}/applications`} className="btn btn-outline btn-small">
                                                View Applications
                                            </Link>
                                            <Link to={`/recruiter/edit-job/${job.id}`} className="btn btn-outline btn-small">
                                                <i className="fas fa-edit"></i>
                                            </Link>
                                            <button
                                                onClick={() => handleDeleteJob(job.id)}
                                                className="btn btn-outline btn-small"
                                                style={{ color: 'var(--danger)', borderColor: 'var(--danger)' }}
                                            >
                                                <i className="fas fa-trash"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default ManageJobs;