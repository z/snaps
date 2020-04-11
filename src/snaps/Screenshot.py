import os
import subprocess
import time

from .Base import Base


class Screenshot(Base):

    def __init__(self):
        super().__init__()

    def capture(self):
        time_string = time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime())
        image_name = f'clipping_{time_string}.png'

        os.chdir(os.path.expanduser(self.config['default']['local_screenshot_path']))

        subprocess.call(['scrot', image_name, '-s'])
        subprocess.call(['mogrify', '-shave', '1x1', image_name])

        return image_name
