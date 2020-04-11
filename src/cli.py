#!/usr/bin/env python3
import argparse

from snaps import __package_name__
from snaps import __version__

from snaps.Notification import ScreenshotNotification
from snaps.Screenshot import Screenshot


def main():

    parser = argparse.ArgumentParser(description='SNAPS uses the notification system to prompt users for an action post-screenshot.')
    parser.add_argument('--version', action='version', version=f'{__package_name__} {__version__}')

    args = parser.parse_args()

    image_name = Screenshot().capture()
    ScreenshotNotification(summary='Screenshot taken',
                           body='What action would you like to take?',
                           user_data={'image_name': image_name})


if __name__ == "__main__":
    main()
