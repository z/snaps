import configparser
import os


def read_config(config_file):

    if not os.path.isfile(config_file):
        print(config_file + ' not found, please create one.')
        return False

    config = configparser.ConfigParser()
    config.read(config_file)

    return config['default']