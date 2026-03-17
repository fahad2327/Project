// // import api from './api';

// // class FreelancerService {
// //     async getDashboard() {
// //         const response = await api.get('/freelancer/dashboard');
// //         return response.data;
// //     }

// //     async getProfile() {
// //         const response = await api.get('/freelancer/profile');
// //         return response.data;
// //     }

// //     async updateProfile(profileData) {
// //         const response = await api.put('/freelancer/profile', profileData);
// //         return response.data;
// //     }

// //     async searchJobs(filters) {
// //         const params = new URLSearchParams(filters).toString();
// //         const response = await api.get(`/freelancer/jobs/search?${params}`);
// //         return response.data;
// //     }

// //     async getJobDetails(jobId) {
// //         const response = await api.get(`/jobs/${jobId}`);
// //         return response.data;
// //     }

// //     async applyForJob(jobId, applicationData) {
// //         const response = await api.post(`/freelancer/jobs/${jobId}/apply`, applicationData);
// //         return response.data;
// //     }

// //     async getApplications() {
// //         const response = await api.get('/freelancer/applications');
// //         return response.data;
// //     }
// // }

// // export default new FreelancerService();
// // freelancerService.js
// import api from './api';

// class FreelancerService {
//     async getDashboard() {
//         const response = await api.get('/freelancer/dashboard');
//         return response.data;
//     }

//     async getProfile() {
//         const response = await api.get('/freelancer/profile');
//         return response.data;
//     }

//     async updateProfile(profileData) {
//         const response = await api.put('/freelancer/profile', profileData);
//         return response.data;
//     }

//     async searchJobs(filters) {
//         const params = new URLSearchParams(filters).toString();
//         const response = await api.get(`/freelancer/jobs/search?${params}`);
//         return response.data;
//     }

//     async getJobDetails(jobId) {
//         const response = await api.get(`/jobs/${jobId}`);
//         return response.data;
//     }

//     async applyForJob(jobId, applicationData) {
//         // Ensure proposed_rate is handled properly
//         const dataToSend = {
//             cover_letter: applicationData.cover_letter,
//             proposed_rate: applicationData.proposed_rate || null,
//             availability_date: applicationData.availability_date || null
//         };
//         console.log('Sending application data:', dataToSend);
//         const response = await api.post(`/freelancer/jobs/${jobId}/apply`, dataToSend);
//         return response.data;
//     }

//     async getApplications() {
//         const response = await api.get('/freelancer/applications');
//         return response.data;
//     }
// }

// export default new FreelancerService();
import api from './api';

class FreelancerService {
    async getDashboard() {
        const response = await api.get('/freelancer/dashboard');
        return response.data;
    }

    async getProfile() {
        const response = await api.get('/freelancer/profile');
        return response.data;
    }

    async updateProfile(profileData) {
        const response = await api.put('/freelancer/profile', profileData);
        return response.data;
    }

    async searchJobs(filters) {
        const params = new URLSearchParams(filters).toString();
        const response = await api.get(`/freelancer/jobs/search?${params}`);
        return response.data;
    }

    async getJobDetails(jobId) {
        const response = await api.get(`/freelancer/jobs/${jobId}`);
        return response.data;
    }

    async applyForJob(jobId, applicationData) {
        const dataToSend = {
            cover_letter: applicationData.cover_letter,
            proposed_rate: applicationData.proposed_rate || null,
            availability_date: applicationData.availability_date || null
        };
        const response = await api.post(`/freelancer/jobs/${jobId}/apply`, applicationData);
        return response.data;
    }

    async getApplications() {
        const response = await api.get('/freelancer/applications');
        return response.data;
    }
}

export default new FreelancerService();