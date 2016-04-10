#!/usr/bin/python
import time
from gi.repository import Notify
from gi.repository import Gtk
from snaps.notifications import *
from snaps.util import *


def main():

    root_dir = os.path.dirname(os.path.realpath(__file__))

    config = read_config(root_dir + '/config.ini')

    time_string = time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime())
    image_pattern = 'clipping_' + time_string + '.png'

    os.chdir(expanduser(config['local_screenshot_path']))

    subprocess.call(['scrot', image_pattern, '-s'])

    # One time initialization of libnotify
    Notify.init('Screenshot clip and upload')

    arguments = {
        'config': config,
        'image_pattern': image_pattern
    }

    icon = "dialog-information"  # dialog-warn, dialog-error
    notification = ScreenshotNotification(summary='Screenshot taken',
                                          body='What action would you like to take?',
                                          icon=icon,
                                          arguments=arguments)
    notification.show()

    notification.connect("closed", Gtk.main_quit)
    Gtk.main()


if __name__ == "__main__":
    main()
