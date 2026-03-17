// import React, { useState, useEffect } from 'react';
// import { useAuth } from '../context/AuthContext';
// import notificationService from '../services/notificationService';
// import './Notifications.css';

// const Notifications = () => {
//     const { user } = useAuth();
//     const [notifications, setNotifications] = useState([]);
//     const [loading, setLoading] = useState(true);
//     const [filter, setFilter] = useState('all'); // all, unread, read
//     const [page, setPage] = useState(1);
//     const [hasMore, setHasMore] = useState(true);

//     useEffect(() => {
//         if (user) {
//             fetchNotifications();
//         }
//     }, [user, filter, page]);

//     const fetchNotifications = async () => {
//         setLoading(true);
//         try {
//             const params = {
//                 limit: 20,
//                 page: page
//             };

//             if (filter === 'unread') {
//                 params.unread_only = true;
//             }

//             const data = await notificationService.getNotifications(params);
//             if (data?.success) {
//                 if (page === 1) {
//                     setNotifications(data.notifications || []);
//                 } else {
//                     setNotifications(prev => [...prev, ...(data.notifications || [])]);
//                 }
//                 setHasMore(data.has_more || false);
//             }
//         } catch (error) {
//             console.error('Error fetching notifications:', error);
//         } finally {
//             setLoading(false);
//         }
//     };

//     const handleMarkAsRead = async (notificationId) => {
//         try {
//             await notificationService.markAsRead(notificationId);
//             setNotifications(prev =>
//                 prev.map(n =>
//                     n.id === notificationId ? { ...n, is_read: true } : n
//                 )
//             );
//         } catch (error) {
//             console.error('Error marking as read:', error);
//         }
//     };

//     const handleMarkAllAsRead = async () => {
//         try {
//             await notificationService.markAllAsRead();
//             setNotifications(prev =>
//                 prev.map(n => ({ ...n, is_read: true }))
//             );
//         } catch (error) {
//             console.error('Error marking all as read:', error);
//         }
//     };

//     const loadMore = () => {
//         if (hasMore && !loading) {
//             setPage(prev => prev + 1);
//         }
//     };

//     const getTimeAgo = (dateString) => {
//         if (!dateString) return '';

//         const date = new Date(dateString);
//         const now = new Date();
//         const diffInSeconds = Math.floor((now - date) / 1000);

//         if (diffInSeconds < 60) return 'just now';
//         if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
//         if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
//         if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
//         return date.toLocaleDateString();
//     };

//     return (
//         <div className="notifications-page">
//             <div className="notifications-header">
//                 <h1>Notifications</h1>
//                 <div className="notification-actions">
//                     <div className="filter-buttons">
//                         <button
//                             className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
//                             onClick={() => { setFilter('all'); setPage(1); }}
//                         >
//                             All
//                         </button>
//                         <button
//                             className={`filter-btn ${filter === 'unread' ? 'active' : ''}`}
//                             onClick={() => { setFilter('unread'); setPage(1); }}
//                         >
//                             Unread
//                         </button>
//                         <button
//                             className={`filter-btn ${filter === 'read' ? 'active' : ''}`}
//                             onClick={() => { setFilter('read'); setPage(1); }}
//                         >
//                             Read
//                         </button>
//                     </div>
//                     <button
//                         onClick={handleMarkAllAsRead}
//                         className="mark-all-btn"
//                         disabled={notifications.every(n => n.is_read)}
//                     >
//                         Mark all as read
//                     </button>
//                 </div>
//             </div>

//             <div className="notifications-list">
//                 {loading && page === 1 ? (
//                     <div className="notifications-loading">
//                         <div className="loader"></div>
//                         <p>Loading notifications...</p>
//                     </div>
//                 ) : notifications.length > 0 ? (
//                     <>
//                         {notifications.map(notification => (
//                             <div
//                                 key={notification.id}
//                                 className={`notification-card ${!notification.is_read ? 'unread' : ''}`}
//                                 onClick={() => !notification.is_read && handleMarkAsRead(notification.id)}
//                             >
//                                 <div className="notification-card-icon"
//                                     style={{
//                                         background: notificationService.getNotificationColor(notification.type)
//                                     }}
//                                 >
//                                     {notificationService.getNotificationIcon(notification.type)}
//                                 </div>
//                                 <div className="notification-card-content">
//                                     <div className="notification-card-header">
//                                         <h3>{notification.title}</h3>
//                                         <span className="notification-card-time">
//                                             {getTimeAgo(notification.created_at)}
//                                         </span>
//                                     </div>
//                                     <p className="notification-card-message">{notification.message}</p>
//                                     {notification.related_data && (
//                                         <div className="notification-card-meta">
//                                             {notification.related_data.job_title && (
//                                                 <span className="meta-tag">Job: {notification.related_data.job_title}</span>
//                                             )}
//                                             {notification.related_data.application_status && (
//                                                 <span className={`status-badge ${notification.related_data.application_status}`}>
//                                                     {notification.related_data.application_status}
//                                                 </span>
//                                             )}
//                                         </div>
//                                     )}
//                                 </div>
//                                 {!notification.is_read && (
//                                     <div className="notification-card-dot"></div>
//                                 )}
//                             </div>
//                         ))}

//                         {hasMore && (
//                             <div className="load-more-container">
//                                 <button
//                                     onClick={loadMore}
//                                     className="load-more-btn"
//                                     disabled={loading}
//                                 >
//                                     {loading ? 'Loading...' : 'Load More'}
//                                 </button>
//                             </div>
//                         )}
//                     </>
//                 ) : (
//                     <div className="notifications-empty">
//                         <i className="fas fa-bell-slash"></i>
//                         <h3>No notifications</h3>
//                         <p>You don't have any notifications at the moment.</p>
//                     </div>
//                 )}
//             </div>
//         </div>
//     );
// };

// export default Notifications;
// src/pages/Notifications.jsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import notificationService from '../services/notificationService';
import './Notifications.css';

const Notifications = () => {
    const { user } = useAuth();
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all');
    const [page, setPage] = useState(1);
    const [hasMore, setHasMore] = useState(false);

    useEffect(() => {
        if (user) {
            fetchNotifications();
        }
    }, [user, filter, page]);

    const fetchNotifications = async () => {
        setLoading(true);
        try {
            const params = {
                limit: 20,
                page: page
            };

            if (filter === 'unread') {
                params.unread_only = true;
            }

            const data = await notificationService.getNotifications(params);
            if (data && data.notifications) {
                if (page === 1) {
                    setNotifications(data.notifications);
                } else {
                    setNotifications(prev => [...prev, ...data.notifications]);
                }
                setHasMore(data.has_more || false);
            }
        } catch (error) {
            console.error('Error fetching notifications:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleMarkAsRead = async (notificationId) => {
        try {
            await notificationService.markAsRead(notificationId);
            setNotifications(prev =>
                prev.map(n =>
                    n.id === notificationId ? { ...n, is_read: true } : n
                )
            );
        } catch (error) {
            console.error('Error marking as read:', error);
        }
    };

    const handleMarkAllAsRead = async () => {
        try {
            await notificationService.markAllAsRead();
            setNotifications(prev =>
                prev.map(n => ({ ...n, is_read: true }))
            );
        } catch (error) {
            console.error('Error marking all as read:', error);
        }
    };

    const getTimeAgo = (dateString) => {
        if (!dateString) return '';
        const date = new Date(dateString);
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);

        if (diffInSeconds < 60) return 'just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
        if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
        return date.toLocaleDateString();
    };

    return (
        <div className="notifications-page">
            <div className="notifications-header">
                <h1>Notifications</h1>
                <div className="notification-actions">
                    <div className="filter-buttons">
                        <button
                            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
                            onClick={() => { setFilter('all'); setPage(1); }}
                        >
                            All
                        </button>
                        <button
                            className={`filter-btn ${filter === 'unread' ? 'active' : ''}`}
                            onClick={() => { setFilter('unread'); setPage(1); }}
                        >
                            Unread
                        </button>
                    </div>
                    <button
                        onClick={handleMarkAllAsRead}
                        className="mark-all-btn"
                        disabled={notifications.every(n => n.is_read)}
                    >
                        Mark all as read
                    </button>
                </div>
            </div>

            <div className="notifications-list">
                {loading && page === 1 ? (
                    <div className="notifications-loading">
                        <div className="loader"></div>
                        <p>Loading notifications...</p>
                    </div>
                ) : notifications.length > 0 ? (
                    <>
                        {notifications.map(notification => (
                            <div
                                key={notification.id}
                                className={`notification-card ${!notification.is_read ? 'unread' : ''}`}
                                onClick={() => !notification.is_read && handleMarkAsRead(notification.id)}
                            >
                                <div className="notification-card-content">
                                    <div className="notification-card-header">
                                        <h3>{notification.title}</h3>
                                        <span className="notification-card-time">
                                            {getTimeAgo(notification.created_at)}
                                        </span>
                                    </div>
                                    <p className="notification-card-message">{notification.message}</p>
                                </div>
                                {!notification.is_read && (
                                    <div className="notification-card-dot"></div>
                                )}
                            </div>
                        ))}

                        {hasMore && (
                            <div className="load-more-container">
                                <button
                                    onClick={() => setPage(prev => prev + 1)}
                                    className="load-more-btn"
                                    disabled={loading}
                                >
                                    {loading ? 'Loading...' : 'Load More'}
                                </button>
                            </div>
                        )}
                    </>
                ) : (
                    <div className="notifications-empty">
                        <i className="fas fa-bell-slash"></i>
                        <h3>No notifications</h3>
                        <p>You don't have any notifications at the moment.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Notifications;