import gi
gi.require_version("Notify", "0.7")
from gi.repository import Notify


def test_notification():
    Notify.init("Test")
    notification = Notify.Notification.new(summary="foo", body="Cool")
    notification.show()
    notification.close()
