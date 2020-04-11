import subprocess
import requests
import json

from base64 import b64encode
from os.path import expanduser

import gi

gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')

from gi.repository import Notify
from gi.repository import Gtk

from .Base import Base

# One time initialization of libnotify
Notify.init('Screenshot clip and upload')


class ScreenshotNotification(Base, Notify.Notification):

    def __init__(self, **kwargs):
        super().__init__()
        """
        :param kwargs:
        """
        Notify.Notification.__init__(self, summary=kwargs['summary'], body=kwargs['body'])

        # icon = dialog-information, dialog-warn, dialog-error
        kwargs['icon'] = 'dialog-information'

        self.add_action(
            action='action_click_upload_image_scp',
            label='Upload',
            callback=self.upload_image_scp,
            user_data=kwargs['user_data']
        )

        self.add_action(
            action='action_click_upload_image_imgur',
            label='Imgur',
            callback=self.upload_image_imgur,
            user_data=kwargs['user_data']
        )

        self.add_action(
            action='action_click_open_in_file_browser',
            label='Files',
            callback=self.open_in_file_browser,
            user_data=None
        )

        self.add_action(
            action='action_click_open_in_gimp',
            label='GIMP',
            callback=self.open_in_gimp,
            user_data=kwargs['user_data']
        )

        self.add_action(
            action='action_click_cancel_upload',
            label='Cancel',
            callback=self.cancel_upload,
            user_data=None
        )

        self.connect('closed', Gtk.main_quit)
        self.show()
        Gtk.main()

    def _open_url(self, url):
        subprocess.call([self.config['default']['web_browser'], url])
        self.done()

    def cancel_upload(self, notification, action, user_data):
        self.done()

    def done(self):
        self.close()
        Notify.uninit()
        Gtk.main_quit()

    def open_in_file_browser(self, notification, action, user_data):
        local_screenshot_path = expanduser(self.config['default']['local_screenshot_path'])
        subprocess.call([self.config['default']['file_browser'], local_screenshot_path])
        self.done()

    def open_in_gimp(self, notification, action, user_data):
        image_name = user_data['image_name']
        local_screenshot_path = expanduser(self.config['default']['local_screenshot_path'])
        subprocess.call(['gimp', local_screenshot_path + image_name])
        self.done()

    def upload_image_scp(self, notification, action, user_data):

        image_name = user_data['image_name']

        local_screenshot_path = expanduser(self.config['default']['local_screenshot_path'])
        remote_screenshot_path = self.config['default']['remote_screenshot_path']
        remote_server_url = self.config['default']['remote_server_url']
        remote_user = self.config['default']['remote_user']
        remote_server = self.config['default']['remote_server']

        subprocess.call(['scp', local_screenshot_path + image_name,
                         remote_user + '@' + remote_server + ':' + remote_screenshot_path])

        url = remote_server_url + image_name

        self._open_url(url)

    def upload_image_imgur(self, notification, action, user_data):

        image_name = user_data['image_name']

        local_screenshot_path = expanduser(self.config['default']['local_screenshot_path'])
        headers = {"Authorization": "Client-ID " + self.config['default']['imgur_client_id']}
        url = 'https://api.imgur.com/3/upload'

        data = {
            'key': self.config['default']['api_key'],
            'image': b64encode(open(local_screenshot_path + image_name, 'rb').read()),
            'type': 'base64',
            'name': image_name,
            'title': image_name
        }

        api_response = requests.post(
            url,
            headers=headers,
            data=data
        )

        response = json.loads(api_response.text)
        self._open_url(response['data']['link'])
