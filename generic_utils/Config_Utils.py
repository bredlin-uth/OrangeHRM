import os
from configparser import ConfigParser

def get_config(section, option):
    config = ConfigParser()
    file = os.path.join(os.path.dirname(os.path.abspath('.')), "test_data\\config.ini")
    config.read(file)
    return config.get(section, option)
