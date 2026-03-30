// // import React from 'react';
// // import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// // import { Toaster } from 'react-hot-toast';
// // import { AuthProvider, useAuth } from './context/AuthContext';

// // // Components
// // import Navbar from './components/common/Navbar';
// // import Footer from './components/common/Footer';
// // import Loader from './components/common/Loader';
// // import LandingPage from './components/home/LandingPage';
// // import Login from './components/Auth/Login';  // Changed from ./components/auth/Login
// // import Register from './components/Auth/Register';  // Changed from ./components/auth/Regist

// // // Freelancer Components
// // import FreelancerDashboard from './components/freelancer/FreelancerDashboard';
// // import FreelancerProfile from './components/freelancer/FreelancerProfile';
// // import JobSearch from './components/freelancer/JobSearch';
// // import JobDetails from './components/freelancer/JobDetails';
// // import MyApplications from './components/freelancer/MyApplications';

// // // Recruiter Components
// // import RecruiterDashboard from './components/recruiter/RecruiterDashboard';
// // import RecruiterProfile from './components/recruiter/RecruiterProfile';
// // import PostJob from './components/recruiter/PostJob';
// // import ManageJobs from './components/recruiter/ManageJobs';
// // import ViewApplications from './components/recruiter/ViewApplications';

// // import './App.css';

// // const PrivateRoute = ({ children, allowedRoles = [] }) => {
// //   const { isAuthenticated, userRole, loading } = useAuth();

// //   if (loading) return <Loader />;

// //   if (!isAuthenticated) {
// //     return <Navigate to="/login" />;
// //   }

// //   if (allowedRoles.length > 0 && !allowedRoles.includes(userRole)) {
// //     return <Navigate to="/" />;
// //   }

// //   return children;
// // };

// // function AppContent() {
// //   const { isAuthenticated, userRole } = useAuth();

// //   return (
// //     <div className="app">
// //       <Navbar />
// //       <main className="main-content">
// //         <Routes>
// //           {/* Public Routes */}
// //           <Route path="/" element={<LandingPage />} />
// //           <Route
// //             path="/login"
// //             element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />}
// //           />
// //           <Route
// //             path="/register"
// //             element={isAuthenticated ? <Navigate to="/dashboard" /> : <Register />}
// //           />

// //           {/* Freelancer Routes */}
// //           <Route
// //             path="/dashboard"
// //             element={
// //               <PrivateRoute allowedRoles={['freelancer', 'recruiter']}>
// //                 {userRole === 'freelancer' ? <FreelancerDashboard /> : <RecruiterDashboard />}
// //               </PrivateRoute>
// //             }
// //           />
// //           <Route
// //             path="/profile"
// //             element={
// //               <PrivateRoute>
// //                 {userRole === 'freelancer' ? <FreelancerProfile /> : <RecruiterProfile />}
// //               </PrivateRoute>
// //             }
// //           />

// //           {/* Freelancer Specific Routes */}
// //           <Route
// //             path="/jobs"
// //             element={
// //               <PrivateRoute allowedRoles={['freelancer']}>
// //                 <JobSearch />
// //               </PrivateRoute>
// //             }
// //           />
// //           <Route
// //             path="/jobs/:jobId"
// //             element={
// //               <PrivateRoute allowedRoles={['freelancer']}>
// //                 <JobDetails />
// //               </PrivateRoute>
// //             }
// //           />
// //           <Route
// //             path="/my-applications"
// //             element={
// //               <PrivateRoute allowedRoles={['freelancer']}>
// //                 <MyApplications />
// //               </PrivateRoute>
// //             }
// //           />

// //           {/* Recruiter Specific Routes */}
// //           <Route
// //             path="/post-job"
// //             element={
// //               <PrivateRoute allowedRoles={['recruiter']}>
// //                 <PostJob />
// //               </PrivateRoute>
// //             }
// //           />
// //           <Route
// //             path="/manage-jobs"
// //             element={
// //               <PrivateRoute allowedRoles={['recruiter']}>
// //                 <ManageJobs />
// //               </PrivateRoute>
// //             }
// //           />
// //           <Route
// //             path="/jobs/:jobId/applications"
// //             element={
// //               <PrivateRoute allowedRoles={['recruiter']}>
// //                 <ViewApplications />
// //               </PrivateRoute>
// //             }
// //           />
// //         </Routes>
// //       </main>
// //       <Footer />
// //       <Toaster position="top-right" />
// //     </div>
// //   );
// // }

// // function App() {
// //   return (
// //     <Router>
// //       <AuthProvider>
// //         <AppContent />
// //       </AuthProvider>
// //     </Router>
// //   );
// // }

// // export default App;
// // src/App.js
// import React from 'react';
// import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// import { Toaster } from 'react-hot-toast';
// import { AuthProvider, useAuth } from './context/AuthContext';

// // Components
// import Navbar from './components/common/Navbar';
// import Footer from './components/common/Footer';
// import Loader from './components/common/Loader';
// import LandingPage from './components/home/LandingPage';
// import Login from './components/Auth/Login';
// import Register from './components/Auth/Register';
// import VerifyEmail from './pages/VerifyEmail'; // Add this import
// import Notifications from './pages/Notifications'; // Add this import

// // Freelancer Components
// import FreelancerDashboard from './components/freelancer/FreelancerDashboard';
// import FreelancerProfile from './components/freelancer/FreelancerProfile';
// import JobSearch from './components/freelancer/JobSearch';
// import JobDetails from './components/freelancer/JobDetails';
// import MyApplications from './components/freelancer/MyApplications';

// // Recruiter Components
// import RecruiterDashboard from './components/recruiter/RecruiterDashboard';
// import RecruiterProfile from './components/recruiter/RecruiterProfile';
// import PostJob from './components/recruiter/PostJob';
// import ManageJobs from './components/recruiter/ManageJobs';
// import ViewApplications from './components/recruiter/ViewApplications';

// import './App.css';

// const PrivateRoute = ({ children, allowedRoles = [] }) => {
//   const { isAuthenticated, userRole, loading } = useAuth();

//   if (loading) return <Loader />;

//   if (!isAuthenticated) {
//     return <Navigate to="/login" />;
//   }

//   if (allowedRoles.length > 0 && !allowedRoles.includes(userRole)) {
//     return <Navigate to="/" />;
//   }

//   return children;
// };

// function AppContent() {
//   const { isAuthenticated, userRole } = useAuth();

//   return (
//     <div className="app">
//       <Navbar />
//       <main className="main-content">
//         <Routes>
//           {/* Public Routes */}
//           <Route path="/" element={<LandingPage />} />
//           <Route
//             path="/login"
//             element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />}
//           />
//           <Route
//             path="/register"
//             element={isAuthenticated ? <Navigate to="/dashboard" /> : <Register />}
//           />
//           <Route path="/verify-email" element={<VerifyEmail />} />
//           <Route path="/verify-email/:token" element={<VerifyEmail />} />

//           {/* Notifications Route - Add this */}
//           <Route
//             path="/notifications"
//             element={
//               <PrivateRoute>
//                 <Notifications />
//               </PrivateRoute>
//             }
//           />

//           {/* Freelancer Routes */}
//           <Route
//             path="/dashboard"
//             element={
//               <PrivateRoute allowedRoles={['freelancer', 'recruiter']}>
//                 {userRole === 'freelancer' ? <FreelancerDashboard /> : <RecruiterDashboard />}
//               </PrivateRoute>
//             }
//           />
//           <Route
//             path="/profile"
//             element={
//               <PrivateRoute>
//                 {userRole === 'freelancer' ? <FreelancerProfile /> : <RecruiterProfile />}
//               </PrivateRoute>
//             }
//           />

//           {/* Freelancer Specific Routes */}
//           <Route
//             path="/jobs"
//             element={
//               <PrivateRoute allowedRoles={['freelancer']}>
//                 <JobSearch />
//               </PrivateRoute>
//             }
//           />
//           <Route
//             path="/jobs/:jobId"
//             element={
//               <PrivateRoute allowedRoles={['freelancer']}>
//                 <JobDetails />
//               </PrivateRoute>
//             }
//           />
//           <Route
//             path="/my-applications"
//             element={
//               <PrivateRoute allowedRoles={['freelancer']}>
//                 <MyApplications />
//               </PrivateRoute>
//             }
//           />

//           {/* Recruiter Specific Routes */}
//           <Route
//             path="/post-job"
//             element={
//               <PrivateRoute allowedRoles={['recruiter']}>
//                 <PostJob />
//               </PrivateRoute>
//             }
//           />
//           <Route
//             path="/manage-jobs"
//             element={
//               <PrivateRoute allowedRoles={['recruiter']}>
//                 <ManageJobs />
//               </PrivateRoute>
//             }
//           />
//           <Route
//             path="/jobs/:jobId/applications"
//             element={
//               <PrivateRoute allowedRoles={['recruiter']}>
//                 <ViewApplications />
//               </PrivateRoute>
//             }
//           />

//           {/* Catch-all route for 404 */}
//           <Route path="*" element={<div>Page Not Found</div>} />
//         </Routes>
//       </main>
//       <Footer />
//       <Toaster position="top-right" />
//     </div>
//   );
// }

// function App() {
//   return (
//     <Router>
//       <AuthProvider>
//         <AppContent />
//       </AuthProvider>
//     </Router>
//   );
// }

// export default App;
// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './context/AuthContext';

// Components
import Navbar from './components/common/Navbar';
import Footer from './components/common/Footer';
import Loader from './components/common/Loader';
import LandingPage from './components/home/LandingPage';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import VerifyEmail from './components/VerifyEmail';
import Notifications from './pages/Notifications';

// Freelancer Components
import FreelancerDashboard from './components/freelancer/FreelancerDashboard';
import FreelancerProfile from './components/freelancer/FreelancerProfile';
import JobSearch from './components/freelancer/JobSearch';
import JobDetails from './components/freelancer/JobDetails';
import MyApplications from './components/freelancer/MyApplications';

// Recruiter Components
import EditJob from './components/recruiter/EditJob';
import RecruiterDashboard from './components/recruiter/RecruiterDashboard';
import RecruiterProfile from './components/recruiter/RecruiterProfile';
import PostJob from './components/recruiter/PostJob';
import ManageJobs from './components/recruiter/ManageJobs';
import ViewApplications from './components/recruiter/ViewApplications';

import './App.css';

// Role-based route guard
const PrivateRoute = ({ children, allowedRoles = [] }) => {
  const { isAuthenticated, user, loading } = useAuth();

  if (loading) return <Loader />;

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  const userRole = user?.user_type;

  if (allowedRoles.length > 0 && !allowedRoles.includes(userRole)) {
    // Redirect to appropriate dashboard based on role
    if (userRole === 'freelancer') {
      return <Navigate to="/freelancer/dashboard" replace />;
    } else if (userRole === 'recruiter') {
      return <Navigate to="/recruiter/dashboard" replace />;
    } else {
      return <Navigate to="/" replace />;
    }
  }

  return children;
};

// Role-based redirect component
const RoleBasedRedirect = () => {
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  const userRole = user?.user_type;

  if (userRole === 'freelancer') {
    return <Navigate to="/freelancer/dashboard" replace />;
  } else if (userRole === 'recruiter') {
    return <Navigate to="/recruiter/dashboard" replace />;
  } else {
    return <Navigate to="/" replace />;
  }
};

function AppContent() {
  const { isAuthenticated, user } = useAuth();
  const userRole = user?.user_type;

  return (
    <div className="app">
      <Navbar />
      <main className="main-content">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<LandingPage />} />
          <Route
            path="/login"
            element={isAuthenticated ? <RoleBasedRedirect /> : <Login />}
          />
          <Route
            path="/register"
            element={isAuthenticated ? <RoleBasedRedirect /> : <Register />}
          />
          <Route path="/verify-email" element={<VerifyEmail />} />
          <Route path="/verify-email/:token" element={<VerifyEmail />} />

          {/* Notifications - Accessible by all authenticated users */}
          <Route
            path="/notifications"
            element={
              <PrivateRoute>
                <Notifications />
              </PrivateRoute>
            }
          />

          {/* Profile - Accessible by all authenticated users */}
          <Route
            path="/profile"
            element={
              <PrivateRoute>
                {userRole === 'freelancer' ? <FreelancerProfile /> : <RecruiterProfile />}
              </PrivateRoute>
            }
          />

          {/* Freelancer Routes */}
          <Route
            path="/freelancer/dashboard"
            element={
              <PrivateRoute allowedRoles={['freelancer']}>
                <FreelancerDashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/freelancer/jobs"
            element={
              <PrivateRoute allowedRoles={['freelancer']}>
                <JobSearch />
              </PrivateRoute>
            }
          />
          <Route
            path="/freelancer/jobs/:jobId"
            element={
              <PrivateRoute allowedRoles={['freelancer']}>
                <JobDetails />
              </PrivateRoute>
            }
          />
          <Route
            path="/freelancer/applications"
            element={
              <PrivateRoute allowedRoles={['freelancer']}>
                <MyApplications />
              </PrivateRoute>
            }
          />

          {/* Recruiter Routes */}
          <Route
            path="/recruiter/dashboard"
            element={
              <PrivateRoute allowedRoles={['recruiter']}>
                <RecruiterDashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/recruiter/post-job"
            element={
              <PrivateRoute allowedRoles={['recruiter']}>
                <PostJob />
              </PrivateRoute>
            }
          />

          <Route
            path="/recruiter/edit-job/:jobId"
            element={
              <PrivateRoute allowedRoles={['recruiter']}>
                <EditJob />
              </PrivateRoute>
            }
          />

          <Route
            path="/recruiter/jobs"
            element={
              <PrivateRoute allowedRoles={['recruiter']}>
                <ManageJobs />
              </PrivateRoute>
            }
          />
          <Route
            path="/recruiter/jobs/:jobId/applications"
            element={
              <PrivateRoute allowedRoles={['recruiter']}>
                <ViewApplications />
              </PrivateRoute>
            }
          />

          {/* Legacy routes - redirect to new role-based routes */}
          <Route
            path="/dashboard"
            element={<RoleBasedRedirect />}
          />
          <Route
            path="/jobs"
            element={
              isAuthenticated ? (
                userRole === 'freelancer' ?
                  <Navigate to="/freelancer/jobs" replace /> :
                  <Navigate to="/recruiter/dashboard" replace />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/jobs/:jobId"
            element={
              isAuthenticated && userRole === 'freelancer' ?
                <JobDetails /> :
                <Navigate to="/login" replace />
            }
          />
          <Route
            path="/my-applications"
            element={
              isAuthenticated && userRole === 'freelancer' ?
                <Navigate to="/freelancer/applications" replace /> :
                <Navigate to="/login" replace />
            }
          />
          <Route
            path="/post-job"
            element={
              isAuthenticated && userRole === 'recruiter' ?
                <Navigate to="/recruiter/post-job" replace /> :
                <Navigate to="/login" replace />
            }
          />
          <Route
            path="/manage-jobs"
            element={
              isAuthenticated && userRole === 'recruiter' ?
                <Navigate to="/recruiter/jobs" replace /> :
                <Navigate to="/login" replace />
            }
          />

          {/* 404 Route */}
          <Route path="*" element={<div className="not-found">Page Not Found</div>} />
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