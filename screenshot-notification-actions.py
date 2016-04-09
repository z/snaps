#!/usr/bin/python
from gi.repository import Notify
from gi.repository import Gtk
import configparser
import subprocess
import time
import os
from os.path import expanduser


def main():

    config = read_config('config.ini')

    time_string = time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime())
    image_pattern = 'clipping_' + time_string + '.png'

    os.chdir(expanduser(config['local_screenshot_path']))

    subprocess.call(['scrot', image_pattern, '-s'])

    # One time initialization of libnotify
    Notify.init('Screenshot clip and upload')

    buttons = [
        {
            'button_text': 'Upload Image',
            'callback': upload_image
        },
        {
            'button_text': 'Open in GIMP',
            'callback': open_in_gimp
        },
        {
            'button_text': 'Cancel',
            'callback': cancel_upload
        }
    ]

    arguments = {
        'config': config,
        'image_pattern': image_pattern
    }

    # icon = "dialog-information"  # dialog-warn, dialog-error
    notification = MyNotification(summary='Screenshot taken', body='What action would you like to take?',
                                  icon='dialog-information', buttons=buttons, arguments=arguments)
    notification.show()

    # Clear all actions with clear_actions()
    # notification.clear_actions()

    Gtk.main()


class MyNotification(Notify.Notification):

    def __init__(self, **kwargs):
        Notify.Notification.__init__(self, summary=kwargs['summary'], body=kwargs['body'])
        # Notify.Notification.__init__(self, summary=kwargs['summary'], body=kwargs['body'], icon=kwargs['icon'])
        if 'buttons' in kwargs:
            for button in kwargs['buttons']:

                print(button['callback'])

                # if button['callback'] == 'upload_image':
                #      callback = upload_image
                #
                # elif button['callback'] == 'open_in_gimp':
                #      callback = open_in_gimp
                #
                # elif button['callback'] == 'cancel_upload':
                #      callback = cancel_upload
                #
                # self.add_action(
                #     "action_click",
                #     button['button_text'],
                #     #button['callback'](self, "action_click", kwargs['arguments']),
                #     #button['callback'],
                #     callback,
                #     kwargs['arguments']
                # )

                self.add_action(
                    "action_click",
                    button['button_text'],
                    #button['callback'](self, "action_click", kwargs['arguments']),
                    #button['callback'],
                    upload_image,
                    kwargs['arguments']
                )


# Define a callback function
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

    print(url)

    buttons = [
        {
            'button_text': 'Open URL',
            'callback': open_url
        }
    ]

    callback_arguments = {
        'url': url
    }

    callback_notification = MyNotification(summary='Successfully uploaded',
                                           body=remote_server_url + image_pattern,
                                           buttons=buttons,
                                           arguments=callback_arguments)

    callback_notification.show()

    #notification.close()
    # Notify.uninit()


def open_url(args):
    print(args)
    print(args['url'])
    subprocess.call(['chromium-browser', args['url']])
    Gtk.main_quit()


# Define a callback function
def open_in_gimp(notification, action, arguments):

    config = arguments['config']
    image_pattern = arguments['image_pattern']

    local_screenshot_path = expanduser(config['local_screenshot_path'])

    # subprocess.call(['gimp', local_screenshot_path + image_pattern])

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
