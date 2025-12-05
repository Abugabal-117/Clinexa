from threading import Lock
from repositories.base_repository import BaseRepository
from models.notification import Notification

class NotificationRepository(BaseRepository):
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        super().__init__('notifications.csv', 'notification_id')
        self._initialized = True

    def get_fieldnames(self):
        return ['notification_id', 'recipient_id', 'message', 'status', 'created_at']

    def to_model(self, data):
        return Notification.from_dict(data)

    def find_by_recipient(self, recipient_id):
        return self.find_by_field('recipient_id', recipient_id)
