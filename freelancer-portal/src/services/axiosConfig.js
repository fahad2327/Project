// // import axios from 'axios';
// // import authService from './authService';

// // const axiosInstance = axios.create({
// //     baseURL: 'http://localhost:5000/api',
// //     headers: {
// //         'Content-Type': 'application/json'
// //     }
// // });

// // // Request interceptor to add token
// // axiosInstance.interceptors.request.use(
// //     (config) => {
// //         const token = authService.getToken();
// //         if (token) {
// //             config.headers.Authorization = `Bearer ${token}`;
// //         }
// //         return config;
// //     },
// //     (error) => {
// //         return Promise.reject(error);
// //     }
// // );

// // // Response interceptor to handle token refresh
// // axiosInstance.interceptors.response.use(
// //     (response) => {
// //         return response;
// //     },
// //     async (error) => {
// //         const originalRequest = error.config;

// //         // If error is 401 and not already retrying
// //         if (error.response?.status === 401 && !originalRequest._retry) {
// //             originalRequest._retry = true;

// //             try {
// //                 // Try to refresh token
// //                 const newToken = await authService.refreshToken();

// //                 if (newToken) {
// //                     // Retry original request with new token
// //                     originalRequest.headers.Authorization = `Bearer ${newToken}`;
// //                     return axiosInstance(originalRequest);
// //                 }
// //             } catch (refreshError) {
// //                 // If refresh fails, logout user
// //                 authService.logout();
// //                 window.location.href = '/signin';
// //                 return Promise.reject(refreshError);
// //             }
// //         }

// //         return Promise.reject(error);
// //     }
// // );

// // export default axiosInstance;
// // services/axiosInstance.js
// import axios from "axios";

// const axiosInstance = axios.create({
//     baseURL: "http://localhost:5000/api",
//     headers: {
//         "Content-Type": "application/json"
//     }
// });

// // Add token automatically to every request
// axiosInstance.interceptors.request.use(
//     (config) => {
//         const token = localStorage.getItem("access_token");
//         if (token) {
//             config.headers.Authorization = `Bearer ${token}`;
//         }
//         return config;
//     },
//     (error) => {
//         return Promise.reject(error);
//     }
// );

// // Handle response errors
// axiosInstance.interceptors.response.use(
//     (response) => response,
//     (error) => {
//         // If 401 Unauthorized, clear localStorage and redirect to login
//         if (error.response && error.response.status === 401) {
//             console.log('Unauthorized access - clearing storage');
//             localStorage.removeItem('access_token');
//             localStorage.removeItem('user');

//             // Only redirect if not already on login page
//             if (!window.location.pathname.includes('/login')) {
//                 window.location.href = '/login';
//             }
//         }
//         return Promise.reject(error);
//     }
// );

// export default axiosInstance;
import axios from "axios";

const axiosInstance = axios.create({
    baseURL: "http://localhost:5000/api",
    headers: {
        "Content-Type": "application/json"
    }
});

// Add token automatically to every request
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Handle response errors
axiosInstance.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            console.log('Unauthorized access - clearing storage');
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            if (!window.location.pathname.includes('/login')) {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;