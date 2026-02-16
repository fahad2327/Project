import axios from 'axios';
import toast from 'react-hot-toast';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Handle token refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                const response = await axios.post(`${API_URL}/auth/refresh`, null, {
                    headers: { Authorization: `Bearer ${refreshToken}` },
                });

                if (response.data.success) {
                    localStorage.setItem('access_token', response.data.access_token);
                    originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;
                    return api(originalRequest);
                }
            } catch (refreshError) {
                // Redirect to login on refresh failure
                localStorage.clear();
                window.location.href = '/login';
                toast.error('Session expired. Please login again.');
            }
        }

        // Handle other errors
        const errorMessage = error.response?.data?.message || 'Something went wrong';
        toast.error(errorMessage);
        return Promise.reject(error);
    }
);

export default api;