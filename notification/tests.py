import pytest
from notification.models import Notification


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

    def test_mark_as_read_notification(self, notification):
        assert notification.is_read is False
        notification.mark_notification_as_read()
        assert notification.is_read is True
