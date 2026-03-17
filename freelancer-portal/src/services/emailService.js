// src/services/emailService.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class EmailService {
    constructor() {
        this.api = axios.create({
            baseURL: API_URL,
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Add token to requests
        this.api.interceptors.request.use(
            config => {
                const token = localStorage.getItem('token') || localStorage.getItem('access_token');
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                }
                return config;
            },
            error => Promise.reject(error)
        );
    }

    /**
     * Send verification email
     * @param {string} email - User's email address
     */
    async sendVerificationEmail(email) {
        try {
            const response = await this.api.post('/auth/send-verification', { email });
            return response.data;
        } catch (error) {
            console.error('Error sending verification email:', error);
            throw error;
        }
    }

    /**
     * Verify email with token
     * @param {string} token - Verification token
     */
    async verifyEmail(token) {
        try {
            const response = await this.api.get(`/auth/verify-email/${token}`);
            return response.data;
        } catch (error) {
            console.error('Error verifying email:', error);
            throw error;
        }
    }

    /**
     * Resend verification email
     */
    async resendVerificationEmail() {
        try {
            const response = await this.api.post('/auth/resend-verification');
            return response.data;
        } catch (error) {
            console.error('Error resending verification:', error);
            throw error;
        }
    }

    /**
     * Send password reset email
     * @param {string} email - User's email address
     */
    async sendPasswordResetEmail(email) {
        try {
            const response = await this.api.post('/auth/forgot-password', { email });
            return response.data;
        } catch (error) {
            console.error('Error sending password reset:', error);
            throw error;
        }
    }

    /**
     * Reset password with token
     * @param {string} token - Reset token
     * @param {string} password - New password
     */
    async resetPassword(token, password) {
        try {
            const response = await this.api.post(`/auth/reset-password/${token}`, { password });
            return response.data;
        } catch (error) {
            console.error('Error resetting password:', error);
            throw error;
        }
    }
}

// Create instance and export (fixes the ESLint warning)
const emailService = new EmailService();
export default emailService;