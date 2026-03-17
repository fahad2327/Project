// services/notificationService.js
import api from './api';

class NotificationService {
    async getNotifications(params = {}) {
        try {
            const queryParams = new URLSearchParams(params).toString();
            const response = await api.get(`/notifications?${queryParams}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching notifications:', error);
            // Return empty data instead of throwing
            return {
                success: false,
                notifications: [],
                unread_count: 0,
                message: error.response?.data?.message || 'Failed to fetch notifications'
            };
        }
    }

    async getUnreadCount() {
        try {
            const response = await api.get('/notifications/unread/count');
            return response.data;
        } catch (error) {
            console.error('Error fetching unread count:', error);
            return { success: false, unread_count: 0 };
        }
    }

    async markAsRead(notificationId) {
        try {
            const response = await api.post(`/notifications/${notificationId}/read`);
            return response.data;
        } catch (error) {
            console.error('Error marking notification as read:', error);
            throw error;
        }
    }

    async markAllAsRead() {
        try {
            const response = await api.post('/notifications/read-all');
            return response.data;
        } catch (error) {
            console.error('Error marking all as read:', error);
            throw error;
        }
    }

    // Real-time notification methods with better error handling
    subscribeToNotifications(userId, callback) {
        if (!userId) return () => { };

        // Use polling with better error handling
        const interval = setInterval(async () => {
            try {
                const response = await this.getUnreadCount();
                if (response?.success && response.unread_count !== undefined) {
                    callback(response.unread_count);
                }
            } catch (error) {
                console.error('Error polling notifications:', error);
            }
        }, 30000); // Poll every 30 seconds

        return () => clearInterval(interval);
    }

    // Get notification icon based on type
    getNotificationIcon(type) {
        const icons = {
            application: '📝',
            job: '💼',
            message: '💬',
            alert: '⚠️',
            success: '✅',
            error: '❌',
            info: 'ℹ️',
            verification: '📧',
            password_reset: '🔑',
            welcome: '👋',
            default: '🔔'
        };
        return icons[type] || icons.default;
    }

    // Get notification color based on type
    getNotificationColor(type) {
        const colors = {
            application: '#6366f1',
            job: '#10b981',
            message: '#8b5cf6',
            alert: '#f59e0b',
            success: '#10b981',
            error: '#ef4444',
            info: '#3b82f6',
            verification: '#f59e0b',
            password_reset: '#ef4444',
            welcome: '#10b981',
            default: '#6366f1'
        };
        return colors[type] || colors.default;
    }
}

const notificationService = new NotificationService();
export default notificationService;