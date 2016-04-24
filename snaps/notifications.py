from gi.repository import Notify
from gi.repository import Gtk
import subprocess
import requests
import json
from base64 import b64encode
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
            'Imgur',
            upload_image_imgur,
            arguments
        )

        self.add_action(
            "action_click_2",
            'Files',
            open_in_file_browser,
            arguments
        )

        self.add_action(
            "action_click_3",
            'GIMP',
            open_in_gimp,
            arguments
        )

        self.add_action(
            "action_click_4",
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


def upload_image_imgur(notification, action, arguments):

    config = arguments['config']
    image_pattern = arguments['image_pattern']

    local_screenshot_path = expanduser(config['local_screenshot_path'])

    headers = {"Authorization": "Client-ID " + config['imgur_client_id']}

    url = "https://api.imgur.com/3/upload"

    data = {
        'key': config['api_key'],
        'image': b64encode(open(local_screenshot_path + image_pattern, 'rb').read()),
        'type': 'base64',
        'name': image_pattern,
        'title': image_pattern
    }

    api_response = requests.post(
        url,
        headers=headers,
        data=data
    )

    response = json.loads(api_response.text)

    url = response['data']['link']

    open_url(url)


def open_url(url):

    subprocess.call(['chromium-browser', url])

    Gtk.main_quit()


# Define a callback function
def open_in_file_browser(notification, action, arguments):

    config = arguments['config']
    image_pattern = arguments['image_pattern']

    local_screenshot_path = expanduser(config['local_screenshot_path'])

    subprocess.call([config['file_browser'], local_screenshot_path])

    notification.close()
    # Notify.uninit()

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