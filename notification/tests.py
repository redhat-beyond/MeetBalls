import pytest
from notification.models import Notification, NotificationType


@pytest.mark.django_db
class TestNotification:
    def test_create_notification(self, notification):
        assert isinstance(notification, Notification)

    def test_persisted_notification_in_database(self, notification):
        assert notification in Notification.objects.all()

    def test_delete_notification_from_database(self, notification):
        notification.delete()
        with pytest.raises(Notification.DoesNotExist):
            Notification.objects.get(pk=notification.pk)

    def test_update_notification_message(self, notification):
        old_id = notification.id
        assert notification.message == 'Test notification'
        notification.message = 'ABCDE'
        notification.save()
        updated_notification = Notification.objects.get(pk=old_id)
        assert updated_notification.message == 'ABCDE'
        assert old_id == notification.id == updated_notification.id

    def test_update_notification_type(self, notification):
        old_id = notification.id
        assert notification.notification_type == NotificationType.WEBSITE
        notification.notification_type = NotificationType.CHAT
        notification.save()
        updated_notification = Notification.objects.get(pk=old_id)
        assert updated_notification.notification_type == NotificationType.CHAT
        assert old_id == notification.id == updated_notification.id

    def test_update_notification_is_read(self, notification):
        old_id = notification.id
        assert notification.is_read is False
        notification.is_read = True
        notification.save()
        updated_notification = Notification.objects.get(pk=old_id)
        assert updated_notification.is_read is True
        assert old_id == notification.id == updated_notification.id
