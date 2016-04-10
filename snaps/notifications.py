from gi.repository import Notify
from gi.repository import Gtk
import subprocess
from os.path import expanduser


class ScreenshotNotification(Notify.Notification):

    def __init__(self, **kwargs):
        Notify.Notification.__init__(self, summary=kwargs['summary'], body=kwargs['body'])

        arguments = kwargs['arguments']

        self.add_action(
            "action_click_0",
            'Upload',
            upload_image,
            arguments
        )

        self.add_action(
            "action_click_1",
            'Open in GIMP',
            open_in_gimp,
            arguments
        )

        self.add_action(
            "action_click_2",
            'Cancel',
            cancel_upload,
            None
        )


def upload_image(notification, action, arguments):

    config = arguments['config']
    image_pattern = arguments['image_pattern']

    local_screenshot_path = expanduser(config['local_screenshot_path'])
    remote_screenshot_path = config['remote_screenshot_path']
    remote_server_url = config['remote_server_url']
    remote_user = config['remote_user']
    remote_server = config['remote_server']

    subprocess.call(['scp', local_screenshot_path + image_pattern,
                     remote_user + '@' + remote_server + ':' + remote_screenshot_path])

    url = remote_server_url + image_pattern

    open_url(url)


def open_url(url):

    subprocess.call(['chromium-browser', url])

    Gtk.main_quit()


# Define a callback function
def open_in_gimp(notification, action, arguments):

    config = arguments['config']
    image_pattern = arguments['image_pattern']

    local_screenshot_path = expanduser(config['local_screenshot_path'])

    subprocess.call(['gimp', local_screenshot_path + image_pattern])

    notification.close()
    # Notify.uninit()

    Gtk.main_quit()


# Define a callback function
def cancel_upload(notification, action, arguments):

    notification.close()
    # Notify.uninit()

    Gtk.main_quit()