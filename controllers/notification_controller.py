from repositories.repository_factory import RepositoryFactory
from models.notification import Notification
import uuid

class NotificationController:
    @staticmethod
    def send_notification(recipient_id, message):
        notification_repo = RepositoryFactory.get_notification_repository()
        
        notification_id = str(uuid.uuid4())[:8]
        
        notification = Notification(
            notification_id=notification_id,
            recipient_id=recipient_id,
            message=message
        )
        
        notification_repo.save(notification)
        return {'success': True, 'notification': notification}

    @staticmethod
    def get_notifications(user_id):
        notification_repo = RepositoryFactory.get_notification_repository()
        notifications = notification_repo.find_by_recipient(user_id)
        # Sort by latest first, assuming created_at is sortable string
        notifications.sort(key=lambda x: x.created_at, reverse=True)
        return {'success': True, 'notifications': notifications}

    @staticmethod
    def mark_read(notification_id):
        notification_repo = RepositoryFactory.get_notification_repository()
        notification = notification_repo.get_by_id(notification_id)
        
        if not notification:
            return {'success': False, 'message': 'Notification not found'}
        
        notification.mark_as_read()
        notification_repo.save(notification)
        return {'success': True, 'message': 'Notification marked as read'}
