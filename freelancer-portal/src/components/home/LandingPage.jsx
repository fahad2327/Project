// import React from 'react';
// import { Link } from 'react-router-dom';
// import { useAuth } from '../../context/AuthContext';
// import './LandingPage.css';

// const LandingPage = () => {
//     const { isAuthenticated } = useAuth();

//     const features = [
//         {
//             icon: '🎯',
//             title: 'Find Perfect Matches',
//             description: 'Connect with top freelancers or find your dream project using our intelligent matching system.'
//         },
//         {
//             icon: '💼',
//             title: 'Post Jobs Free',
//             description: 'Recruiters can post unlimited job listings and reach thousands of qualified freelancers.'
//         },
//         {
//             icon: '⚡',
//             title: 'Quick Applications',
//             description: 'Apply to jobs with one click and track your applications in real-time.'
//         },
//         {
//             icon: '🔒',
//             title: 'Secure Platform',
//             description: 'Your data is protected with enterprise-grade security and encryption.'
//         },
//         {
//             icon: '📊',
//             title: 'Analytics Dashboard',
//             description: 'Get insights into your applications, hires, and platform performance.'
//         },
//         {
//             icon: '💬',
//             title: 'Instant Notifications',
//             description: 'Receive real-time updates on job applications, status changes, and more.'
//         }
//     ];

//     const stats = [
//         { value: '10K+', label: 'Active Freelancers' },
//         { value: '5K+', label: 'Jobs Posted' },
//         { value: '15K+', label: 'Successful Hires' },
//         { value: '98%', label: 'Satisfaction Rate' }
//     ];

//     return (
//         <div className="landing-page">
//             {/* Hero Section */}
//             <section className="hero-section">
//                 <div className="hero-content">
//                     <h1 className="hero-title">
//                         Connect with Top <span className="gradient-text">Freelancers</span> &
//                         Find Your Next <span className="gradient-text">Opportunity</span>
//                     </h1>
//                     <p className="hero-subtitle">
//                         The premier platform connecting talented freelancers with innovative companies.
//                         Post jobs, find work, and grow your career.
//                     </p>
//                     <div className="hero-buttons">
//                         {!isAuthenticated ? (
//                             <>
//                                 <Link to="/register" className="btn btn-primary btn-large">
//                                     Get Started
//                                 </Link>
//                                 <Link to="/login" className="btn btn-outline btn-large">
//                                     Sign In
//                                 </Link>
//                             </>
//                         ) : (
//                             <Link to="/dashboard" className="btn btn-primary btn-large">
//                                 Go to Dashboard
//                             </Link>
//                         )}
//                     </div>
//                     <div className="hero-stats">
//                         {stats.map((stat, index) => (
//                             <div key={index} className="stat-item">
//                                 <div className="stat-value">{stat.value}</div>
//                                 <div className="stat-label">{stat.label}</div>
//                             </div>
//                         ))}
//                     </div>
//                 </div>
//                 <div className="hero-image">
//                     <img src="/images/hero-illustration.svg" alt="Hero" />
//                 </div>
//             </section>

//             {/* Features Section */}
//             <section className="features-section">
//                 <div className="section-header">
//                     <h2>Why Choose Our Platform?</h2>
//                     <p>Everything you need to succeed in the gig economy</p>
//                 </div>
//                 <div className="features-grid">
//                     {features.map((feature, index) => (
//                         <div key={index} className="feature-card">
//                             <div className="feature-icon">{feature.icon}</div>
//                             <h3>{feature.title}</h3>
//                             <p>{feature.description}</p>
//                         </div>
//                     ))}
//                 </div>
//             </section>

//             {/* How It Works */}
//             <section className="how-it-works">
//                 <div className="section-header">
//                     <h2>How It Works</h2>
//                     <p>Get started in three simple steps</p>
//                 </div>
//                 <div className="steps-container">
//                     <div className="step">
//                         <div className="step-number">1</div>
//                         <h3>Create Your Account</h3>
//                         <p>Sign up as a freelancer or recruiter in less than 2 minutes</p>
//                     </div>
//                     <div className="step">
//                         <div className="step-number">2</div>
//                         <h3>Build Your Profile</h3>
//                         <p>Showcase your skills, experience, or company culture</p>
//                     </div>
//                     <div className="step">
//                         <div className="step-number">3</div>
//                         <h3>Start Connecting</h3>
//                         <p>Post jobs, apply for opportunities, and grow your network</p>
//                     </div>
//                 </div>
//             </section>

//             {/* CTA Section */}
//             <section className="cta-section">
//                 <div className="cta-content">
//                     <h2>Ready to Start Your Journey?</h2>
//                     <p>Join thousands of freelancers and companies already using our platform</p>
//                     {!isAuthenticated ? (
//                         <Link to="/register" className="btn btn-primary btn-large">
//                             Create Free Account
//                         </Link>
//                     ) : (
//                         <Link to="/dashboard" className="btn btn-primary btn-large">
//                             Go to Dashboard
//                         </Link>
//                     )}
//                 </div>
//             </section>
//         </div>
//     );
// };

// export default LandingPage;

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './LandingPage.css';

const LandingPage = () => {
    const { isAuthenticated } = useAuth();
    const [showMainContent, setShowMainContent] = useState(false);

    const features = [
        {
            icon: '🎯',
            title: 'Find Perfect Matches',
            description: 'Connect with top freelancers or find your dream project using our intelligent matching system.'
        },
        {
            icon: '💼',
            title: 'Post Jobs Free',
            description: 'Recruiters can post unlimited job listings and reach thousands of qualified freelancers.'
        },
        {
            icon: '⚡',
            title: 'Quick Applications',
            description: 'Apply to jobs with one click and track your applications in real-time.'
        },
        {
            icon: '🔒',
            title: 'Secure Platform',
            description: 'Your data is protected with enterprise-grade security and encryption.'
        },
        {
            icon: '📊',
            title: 'Analytics Dashboard',
            description: 'Get insights into your applications, hires, and platform performance.'
        },
        {
            icon: '💬',
            title: 'Instant Notifications',
            description: 'Receive real-time updates on job applications, status changes, and more.'
        }
    ];

    const stats = [
        { value: '10K+', label: 'Active Freelancers' },
        { value: '5K+', label: 'Jobs Posted' },
        { value: '15K+', label: 'Successful Hires' },
        { value: '98%', label: 'Satisfaction Rate' }
    ];

    // If showing main content, render the full landing page
    if (showMainContent) {
        return (
            <div className="landing-page">
                {/* Hero Section */}
                <section className="hero-section">
                    <div className="hero-content">
                        <h1 className="hero-title">
                            Connect with Top <span className="gradient-text">Freelancers</span> &
                            Find Your Next <span className="gradient-text">Opportunity</span>
                        </h1>
                        <p className="hero-subtitle">
                            The premier platform connecting talented freelancers with innovative companies.
                            Post jobs, find work, and grow your career.
                        </p>
                        <div className="hero-buttons">
                            {!isAuthenticated ? (
                                <>
                                    <Link to="/register" className="btn btn-primary btn-large">
                                        Get Started
                                    </Link>
                                    <Link to="/login" className="btn btn-outline btn-large">
                                        Sign In
                                    </Link>
                                </>
                            ) : (
                                <Link to="/dashboard" className="btn btn-primary btn-large">
                                    Go to Dashboard
                                </Link>
                            )}
                        </div>
                        <div className="hero-stats">
                            {stats.map((stat, index) => (
                                <div key={index} className="stat-item">
                                    <div className="stat-value">{stat.value}</div>
                                    <div className="stat-label">{stat.label}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="hero-image">
                        <img
                            src="https://img.freepik.com/free-vector/job-interview-concept-illustration_114360-5400.jpg"
                            alt="Job interview process"
                        />
                    </div>
                </section>

                {/* Features Section */}
                <section className="features-section">
                    <div className="section-header">
                        <h2>Why Choose Our Platform?</h2>
                        <p>Everything you need to succeed in the gig economy</p>
                    </div>
                    <div className="features-grid">
                        {features.map((feature, index) => (
                            <div key={index} className="feature-card">
                                <div className="feature-icon">{feature.icon}</div>
                                <h3>{feature.title}</h3>
                                <p>{feature.description}</p>
                            </div>
                        ))}
                    </div>
                </section>

                {/* How It Works */}
                <section className="how-it-works">
                    <div className="section-header">
                        <h2>How It Works</h2>
                        <p>Get started in three simple steps</p>
                    </div>
                    <div className="steps-container">
                        <div className="step">
                            <div className="step-number">1</div>
                            <h3>Create Your Account</h3>
                            <p>Sign up as a freelancer or recruiter in less than 2 minutes</p>
                        </div>
                        <div className="step">
                            <div className="step-number">2</div>
                            <h3>Build Your Profile</h3>
                            <p>Showcase your skills, experience, or company culture</p>
                        </div>
                        <div className="step">
                            <div className="step-number">3</div>
                            <h3>Start Connecting</h3>
                            <p>Post jobs, apply for opportunities, and grow your network</p>
                        </div>
                    </div>
                </section>

                {/* CTA Section */}
                <section className="cta-section">
                    <div className="cta-content">
                        <h2>Ready to Start Your Journey?</h2>
                        <p>Join thousands of freelancers and companies already using our platform</p>
                        {!isAuthenticated ? (
                            <Link to="/register" className="btn btn-primary btn-large">
                                Create Free Account
                            </Link>
                        ) : (
                            <Link to="/dashboard" className="btn btn-primary btn-large">
                                Go to Dashboard
                            </Link>
                        )}
                    </div>
                </section>
            </div>
        );
    }

    // Welcome Screen (Full Screen)
    return (
        <div className="welcome-screen">
            <div className="welcome-content">
                <div className="welcome-logo">
                    <span className="logo-icon">⚡</span>
                    <span className="logo-text">FreelanceHub</span>
                </div>

                <h1 className="welcome-title">
                    Welcome to <span className="gradient-text">FreelanceHub</span>
                </h1>

                <p className="welcome-subtitle">
                    The ultimate platform connecting talented freelancers with innovative companies.
                    Start your journey today!
                </p>

                <div className="welcome-features">
                    <div className="welcome-feature">
                        <div className="feature-icon">💼</div>
                        <div>
                            <h3>For Freelancers</h3>
                            <p>Find work, showcase skills, and grow your career</p>
                        </div>
                    </div>
                    <div className="welcome-feature">
                        <div className="feature-icon">🏢</div>
                        <div>
                            <h3>For Recruiters</h3>
                            <p>Post jobs and find talented professionals</p>
                        </div>
                    </div>
                    <div className="welcome-feature">
                        <div className="feature-icon">🚀</div>
                        <div>
                            <h3>For Everyone</h3>
                            <p>Secure, fast, and easy to use platform</p>
                        </div>
                    </div>
                </div>

                <button
                    onClick={() => setShowMainContent(true)}
                    className="btn btn-primary btn-start"
                >
                    Get Started
                    <i className="fas fa-arrow-right"></i>
                </button>

                <div className="welcome-footer">
                    <p>Already have an account? <Link to="/login">Sign In</Link></p>
                </div>
            </div>

            <div className="welcome-background">
                <div className="shape shape-1"></div>
                <div className="shape shape-2"></div>
                <div className="shape shape-3"></div>
            </div>
        </div>
    );
};

export default LandingPage;