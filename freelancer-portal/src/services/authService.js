// // // // import api from './api';

// // // // class AuthService {
// // // //     async register(userData) {
// // // //         const response = await api.post('/auth/register', userData);
// // // //         if (response.data.success) {
// // // //             localStorage.setItem('access_token', response.data.access_token);
// // // //             localStorage.setItem('refresh_token', response.data.refresh_token);
// // // //             localStorage.setItem('user', JSON.stringify(response.data.user));
// // // //         }
// // // //         return response.data;
// // // //     }

// // // //     async login(credentials) {
// // // //         const response = await api.post('/auth/login', credentials);
// // // //         if (response.data.success) {
// // // //             localStorage.setItem('access_token', response.data.access_token);
// // // //             localStorage.setItem('refresh_token', response.data.refresh_token);
// // // //             localStorage.setItem('user', JSON.stringify(response.data.user));
// // // //         }
// // // //         return response.data;
// // // //     }

// // // //     async logout() {
// // // //         localStorage.removeItem('access_token');
// // // //         localStorage.removeItem('refresh_token');
// // // //         localStorage.removeItem('user');
// // // //         window.location.href = '/login';
// // // //     }

// // // //     getCurrentUser() {
// // // //         const userStr = localStorage.getItem('user');
// // // //         return userStr ? JSON.parse(userStr) : null;
// // // //     }

// // // //     isAuthenticated() {
// // // //         return !!localStorage.getItem('access_token');
// // // //     }

// // // //     getUserRole() {
// // // //         const user = this.getCurrentUser();
// // // //         return user?.user_type || null;
// // // //     }
// // // // }

// // // // const authService = new AuthService();
// // // // export default authService;
// // // // services/authService.js
// // // import api from './api';

// // // class AuthService {
// // //     async login(credentials) {
// // //         try {
// // //             const response = await api.post('/auth/login', credentials);

// // //             if (response.data.success) {
// // //                 // Store tokens and user data
// // //                 localStorage.setItem('access_token', response.data.token); // Make sure this matches your API response
// // //                 localStorage.setItem('user', JSON.stringify(response.data.user));

// // //                 console.log('Login successful, data stored:', response.data);
// // //             }
// // //             return response.data;
// // //         } catch (error) {
// // //             console.error('Login service error:', error);
// // //             throw error;
// // //         }
// // //     }

// // //     async register(userData) {
// // //         try {
// // //             const response = await api.post('/auth/register', userData);

// // //             if (response.data.success) {
// // //                 localStorage.setItem('access_token', response.data.token);
// // //                 localStorage.setItem('user', JSON.stringify(response.data.user));
// // //             }
// // //             return response.data;
// // //         } catch (error) {
// // //             console.error('Register service error:', error);
// // //             throw error;
// // //         }
// // //     }

// // //     logout() {
// // //         localStorage.removeItem('access_token');
// // //         localStorage.removeItem('user');
// // //     }

// // //     getCurrentUser() {
// // //         const userStr = localStorage.getItem('user');
// // //         if (userStr) {
// // //             try {
// // //                 return JSON.parse(userStr);
// // //             } catch {
// // //                 return null;
// // //             }
// // //         }
// // //         return null;
// // //     }

// // //     getToken() {
// // //         return localStorage.getItem('access_token');
// // //     }

// // //     isAuthenticated() {
// // //         return !!this.getToken();
// // //     }
// // // }

// // // const authService = new AuthService();
// // // export default authService;


// // // services/authService.js
// // import api from './api';

// // class AuthService {
// //     async login(credentials) {
// //         try {
// //             const response = await api.post('/auth/login', credentials);
// //             if (response.data.success) {
// //                 localStorage.setItem('access_token', response.data.token); // token from backend
// //                 localStorage.setItem('user', JSON.stringify(response.data.user));
// //             }
// //             return response.data;
// //         } catch (error) {
// //             console.error('Login service error:', error);
// //             throw error;
// //         }
// //     }

// //     async register(userData) {
// //         try {
// //             const response = await api.post('/auth/register', userData);
// //             if (response.data.success) {
// //                 localStorage.setItem('access_token', response.data.token);
// //                 localStorage.setItem('user', JSON.stringify(response.data.user));
// //             }
// //             return response.data;
// //         } catch (error) {
// //             console.error('Register service error:', error);
// //             throw error;
// //         }
// //     }

// //     logout() {
// //         localStorage.removeItem('access_token');
// //         localStorage.removeItem('user');
// //     }

// //     getCurrentUser() {
// //         const userStr = localStorage.getItem('user');
// //         if (userStr) {
// //             try {
// //                 return JSON.parse(userStr);
// //             } catch {
// //                 return null;
// //             }
// //         }
// //         return null;
// //     }

// //     getToken() {
// //         return localStorage.getItem('access_token');
// //     }

// //     isAuthenticated() {
// //         return !!this.getToken();
// //     }
// // }

// // const authService = new AuthService();
// // export default authService;
// import api from './api';

// class AuthService {
//     async login(credentials) {
//         const response = await api.post('/auth/login', credentials);
//         if (response.data.success) {
//             localStorage.setItem('access_token', response.data.token);
//             localStorage.setItem('user', JSON.stringify(response.data.user));
//         }
//         return response.data;
//     }

//     async register(userData) {
//         const response = await api.post('/auth/register', userData);
//         if (response.data.success) {
//             localStorage.setItem('access_token', response.data.token);
//             localStorage.setItem('user', JSON.stringify(response.data.user));
//         }
//         return response.data;
//     }

//     logout() {
//         localStorage.removeItem('access_token');
//         localStorage.removeItem('user');
//         window.location.href = '/login';
//     }

//     getCurrentUser() {
//         const userStr = localStorage.getItem('user');
//         return userStr ? JSON.parse(userStr) : null;
//     }

//     getToken() {
//         return localStorage.getItem('access_token');
//     }

//     isAuthenticated() {
//         return !!this.getToken();
//     }
// }

// export default new AuthService();
import api from './api';

class AuthService {
    async login(credentials) {
        try {
            const response = await api.post('/auth/login', credentials);
            if (response.data.success) {
                localStorage.setItem('access_token', response.data.token);
                localStorage.setItem('user', JSON.stringify(response.data.user));
            }
            return response.data;
        } catch (error) {
            console.error('Login service error:', error);
            throw error;
        }
    }

    async register(userData) {
        try {
            const response = await api.post('/auth/register', userData);
            if (response.data.success) {
                localStorage.setItem('access_token', response.data.token);
                localStorage.setItem('user', JSON.stringify(response.data.user));
            }
            return response.data;
        } catch (error) {
            console.error('Register service error:', error);
            throw error;
        }
    }

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
    }

    getCurrentUser() {
        const userStr = localStorage.getItem('user');
        if (userStr) {
            try {
                return JSON.parse(userStr);
            } catch {
                return null;
            }
        }
        return null;
    }

    getToken() {
        return localStorage.getItem('access_token');
    }

    isAuthenticated() {
        return !!this.getToken();
    }
}

const authService = new AuthService();
export default authService;