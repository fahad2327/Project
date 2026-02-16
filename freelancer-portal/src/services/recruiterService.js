import api from './api';

class RecruiterService {
    async getDashboard() {
        const response = await api.get('/recruiter/dashboard');
        return response.data;
    }

    async getProfile() {
        const response = await api.get('/recruiter/profile');
        return response.data;
    }

    async updateProfile(profileData) {
        const response = await api.put('/recruiter/profile', profileData);
        return response.data;
    }

    async createJob(jobData) {
        const response = await api.post('/recruiter/jobs', jobData);
        return response.data;
    }

    async getMyJobs() {
        const response = await api.get('/recruiter/jobs');
        return response.data;
    }

    async getJobApplications(jobId) {
        const response = await api.get(`/recruiter/jobs/${jobId}/applications`);
        return response.data;
    }

    async updateApplicationStatus(applicationId, statusData) {
        const response = await api.put(`/recruiter/applications/${applicationId}/status`, statusData);
        return response.data;
    }
}

export default new RecruiterService();