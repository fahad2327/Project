import api from './api';

class AuthService {
    async register(userData) {
        const response = await api.post('/auth/register', userData);
        if (response.data.success) {
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('refresh_token', response.data.refresh_token);
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
        return response.data;
    }

    async login(credentials) {
        const response = await api.post('/auth/login', credentials);
        if (response.data.success) {
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('refresh_token', response.data.refresh_token);
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
        return response.data;
    }

    async logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
    }

    getCurrentUser() {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    }

    isAuthenticated() {
        return !!localStorage.getItem('access_token');
    }

    getUserRole() {
        const user = this.getCurrentUser();
        return user?.user_type || null;
    }
}

const authService = new AuthService();
export default authService;