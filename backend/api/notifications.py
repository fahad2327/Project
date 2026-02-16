from flask import Blueprint, request, jsonify
from database.models import Notification
from utils.auth_utils import token_required

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

@notifications_bp.route('', methods=['GET'])
@token_required
def get_notifications():
    """Get user notifications"""
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    limit = request.args.get('limit', 50, type=int)
    
    notifications = Notification.get_by_user(
        request.user_id,
        unread_only=unread_only,
        limit=limit
    )
    
    return jsonify({
        'success': True,
        'count': len(notifications),
        'notifications': notifications
    }), 200

@notifications_bp.route('/unread/count', methods=['GET'])
@token_required
def get_unread_count():
    """Get unread notifications count"""
    count = Notification.get_unread_count(request.user_id)
    
    return jsonify({
        'success': True,
        'unread_count': count
    }), 200

@notifications_bp.route('/<int:notification_id>/read', methods=['POST'])
@token_required
def mark_as_read(notification_id):
    """Mark notification as read"""
    success = Notification.mark_as_read(notification_id, request.user_id)
    
    if not success:
        return jsonify({
            'success': False,
            'message': 'Notification not found'
        }), 404
    
    return jsonify({
        'success': True,
        'message': 'Notification marked as read'
    }), 200

@notifications_bp.route('/read-all', methods=['POST'])
@token_required
def mark_all_as_read():
    """Mark all notifications as read"""
    count = Notification.mark_all_as_read(request.user_id)
    
    return jsonify({
        'success': True,
        'message': f'{count} notifications marked as read'
    }), 200