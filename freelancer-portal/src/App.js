import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './context/AuthContext';

// Components
import Navbar from './components/common/Navbar';
import Footer from './components/common/Footer';
import Loader from './components/common/Loader';
import LandingPage from './components/home/LandingPage';
import Login from './components/Auth/Login';  // Changed from ./components/auth/Login
import Register from './components/Auth/Register';  // Changed from ./components/auth/Regist

// Freelancer Components
import FreelancerDashboard from './components/freelancer/FreelancerDashboard';
import FreelancerProfile from './components/freelancer/FreelancerProfile';
import JobSearch from './components/freelancer/JobSearch';
import JobDetails from './components/freelancer/JobDetails';
import MyApplications from './components/freelancer/MyApplications';

// Recruiter Components
import RecruiterDashboard from './components/recruiter/RecruiterDashboard';
import RecruiterProfile from './components/recruiter/RecruiterProfile';
import PostJob from './components/recruiter/PostJob';
import ManageJobs from './components/recruiter/ManageJobs';
import ViewApplications from './components/recruiter/ViewApplications';

import './App.css';

const PrivateRoute = ({ children, allowedRoles = [] }) => {
  const { isAuthenticated, userRole, loading } = useAuth();

  if (loading) return <Loader />;

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  if (allowedRoles.length > 0 && !allowedRoles.includes(userRole)) {
    return <Navigate to="/" />;
  }

  return children;
};

function AppContent() {
  const { isAuthenticated, userRole } = useAuth();

  return (
    <div className="app">
      <Navbar />
      <main className="main-content">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<LandingPage />} />
          <Route
            path="/login"
            element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />}
          />
          <Route
            path="/register"
            element={isAuthenticated ? <Navigate to="/dashboard" /> : <Register />}
          />

          {/* Freelancer Routes */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute allowedRoles={['freelancer', 'recruiter']}>
                {userRole === 'freelancer' ? <FreelancerDashboard /> : <RecruiterDashboard />}
              </PrivateRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <PrivateRoute>
                {userRole === 'freelancer' ? <FreelancerProfile /> : <RecruiterProfile />}
              </PrivateRoute>
            }
          />

          {/* Freelancer Specific Routes */}
          <Route
            path="/jobs"
            element={
              <PrivateRoute allowedRoles={['freelancer']}>
                <JobSearch />
              </PrivateRoute>
            }
          />
          <Route
            path="/jobs/:jobId"
            element={
              <PrivateRoute allowedRoles={['freelancer']}>
                <JobDetails />
              </PrivateRoute>
            }
          />
          <Route
            path="/my-applications"
            element={
              <PrivateRoute allowedRoles={['freelancer']}>
                <MyApplications />
              </PrivateRoute>
            }
          />

          {/* Recruiter Specific Routes */}
          <Route
            path="/post-job"
            element={
              <PrivateRoute allowedRoles={['recruiter']}>
                <PostJob />
              </PrivateRoute>
            }
          />
          <Route
            path="/manage-jobs"
            element={
              <PrivateRoute allowedRoles={['recruiter']}>
                <ManageJobs />
              </PrivateRoute>
            }
          />
          <Route
            path="/jobs/:jobId/applications"
            element={
              <PrivateRoute allowedRoles={['recruiter']}>
                <ViewApplications />
              </PrivateRoute>
            }
          />
        </Routes>
      </main>
      <Footer />
      <Toaster position="top-right" />
    </div>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App;