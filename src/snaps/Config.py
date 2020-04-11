import configparser
import logging
import os
import pkg_resources
import sys

from shutil import copyfile

from . import __package_name__

logging.basicConfig(stream=sys.stdout)


class Config:
    __instance = None

    def __init__(self):

        if Config.__instance is not None:
            raise Exception('This class is a singleton.  Use .get_instance() instead')
        else:
            Config.__instance = self

        config_path = os.path.expanduser(f'~/.config/{__package_name__}')
        config_file = os.path.join(config_path, f'{config_path}/config.ini')
        config_file_template = '../../config/example.config.ini'

        if not os.path.isfile(config_file):
            print(f'{config_file} not found, and has been created.  Please edit.')
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            copyfile(pkg_resources.resource_filename(__package_name__, config_file_template), config_file)
            raise SystemExit

        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    @staticmethod
    def get_instance():
        if Config.__instance is None:
            Config()
        return Config.__instance

    @staticmethod
    def reset():
        Config.__instance = None
