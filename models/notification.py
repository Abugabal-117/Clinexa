from datetime import datetime

class Notification:
    def __init__(self, notification_id, recipient_id, message, status='unread', created_at=None):
        self.notification_id = notification_id
        self.recipient_id = recipient_id
        self.message = message
        self.status = status
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def mark_as_read(self):
        self.status = 'read'

    @classmethod
    def from_dict(cls, data):
        return cls(
            notification_id=data.get('notification_id'),
            recipient_id=data.get('recipient_id'),
            message=data.get('message'),
            status=data.get('status', 'unread'),
            created_at=data.get('created_at')
        )

    def to_dict(self):
        return {
            'notification_id': self.notification_id,
            'recipient_id': self.recipient_id,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at
        }
