import api from './api';

class NotificationService {
    async getNotifications(params = {}) {
        const queryParams = new URLSearchParams(params).toString();
        const response = await api.get(`/notifications?${queryParams}`);
        return response.data;
    }

    async getUnreadCount() {
        const response = await api.get('/notifications/unread/count');
        return response.data;
    }

    async markAsRead(notificationId) {
        const response = await api.post(`/notifications/${notificationId}/read`);
        return response.data;
    }

    async markAllAsRead() {
        const response = await api.post('/notifications/read-all');
        return response.data;
    }
}

export default new NotificationService();