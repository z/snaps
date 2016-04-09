#!/usr/bin/python
from gi.repository import Notify
from gi.repository import Gtk
import configparser
import subprocess
import time
import os
from os.path import expanduser


def main():

    root_dir = os.path.dirname(os.path.realpath(__file__))

    config = read_config(root_dir + '/config.ini')

    time_string = time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime())
    image_pattern = 'clipping_' + time_string + '.png'

    os.chdir(expanduser(config['local_screenshot_path']))

    subprocess.call(['scrot', image_pattern, '-s'])

    # One time initialization of libnotify
    Notify.init('Screenshot clip and upload')

    buttons = []
    # buttons = [
    #     {
    #         'button_text': 'Upload Image',
    #         'callback': upload_image
    #     },
    #     {
    #         'button_text': 'Open in GIMP',
    #         'callback': open_in_gimp
    #     },
    #     {
    #         'button_text': 'Cancel',
    #         'callback': cancel_upload
    #     },
    # ]

    arguments = {
        'config': config,
        'image_pattern': image_pattern
    }

    icon = "dialog-information"  # dialog-warn, dialog-error
    notification = ScreenshotNotification(summary='Screenshot taken',
                                          body='What action would you like to take?',
                                          icon='dialog-information',
                                          buttons=buttons,
                                          arguments=arguments)
    notification.show()

    notification.connect("closed", Gtk.main_quit)
    Gtk.main()
    

class ScreenshotNotification(Notify.Notification):

    def __init__(self, **kwargs):
        Notify.Notification.__init__(self, summary=kwargs['summary'], body=kwargs['body'])
        # Notify.Notification.__init__(self, summary=kwargs['summary'], body=kwargs['body'], icon=kwargs['icon'])

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


class SuccessNotification(Notify.Notification):

    def __init__(self, **kwargs):
        Notify.Notification.__init__(self, summary=kwargs['summary'], body=kwargs['body'])

        arguments = kwargs['arguments']

        self.add_action(
            "action_click_4",
            'Open URL',
            open_in_gimp,
            arguments
        )


class NotificationFactory(Notify.Notification):

    def __init__(self, **kwargs):
        Notify.Notification.__init__(self, summary=kwargs['summary'], body=kwargs['body'])
        # Notify.Notification.__init__(self, summary=kwargs['summary'], body=kwargs['body'], icon=kwargs['icon'])

        arguments = kwargs['arguments']

        self.add_action(
            "action_click_0",
            'Open in GIMP',
            open_in_gimp,
            arguments
        )

        self.add_action(
            "action_click_1",
            'Upload',
            upload_image,
            arguments
        )

        self.add_action(
            "action_click_2",
            'Cancel',
            cancel_upload,
            None
        )

        # if 'buttons' in kwargs:
        #     i = 0
        #     for button in kwargs['buttons']:
        #         arguments = kwargs['arguments']
        #         callback = button['callback']
        #
        #         self.add_action(
        #             "action_click",
        #             button['button_text'],
        #             # button['callback'](self, "action_click", kwargs['arguments']),
        #             # callback['callback'](self, "action_click", kwargs['arguments']),
        #             callback(self, "action_click_" + str(i), arguments),
        #             # button['callback'],
        #             #button['callback'],
        #             arguments
        #         )
        #         i += 1
        #
        #     subprocess.call(['chromium-browser', 'http://google.com'])


def upload_image(notification, action, arguments):

    # Clear all actions with clear_actions()
    notification.clear_actions()
    notification.close()

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

    arguments = {
        'url': url
    }

    open_url(url)

    # arguments = {
    #     'config': config,
    #     'image_pattern': image_pattern,
    #     'url': url
    # }
    #
    # callback_notification = SuccessNotification(summary='Successfully uploaded!',
    #                                             body=remote_server_url + image_pattern,
    #                                             arguments=arguments)
    #
    # callback_notification.show()
    #
    # callback_notification.connect("closed", Gtk.main_quit)

    # Notify.uninit()
    # Gtk.main_quit()


def open_url(url):

    subprocess.call(['chromium-browser', url])
    # subprocess.call(['chromium-browser', arguments['url']])

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


def read_config(config_file):

    if not os.path.isfile(config_file):
        print(config_file + ' not found, please create one.')
        return False

    config = configparser.ConfigParser()
    config.read(config_file)

    return config['default']


if __name__ == "__main__":
    main()
