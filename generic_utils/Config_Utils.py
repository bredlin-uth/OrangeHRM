import os
import time
from configparser import ConfigParser

config_path = os.path.join(os.path.dirname(os.path.abspath('.')), "test_data\\config.ini")

def get_config(section, option):
    config = ConfigParser()
    config.read(config_path)
    return config.get(section, option)

def change_properties_file(section, property_name, property_value):
    flag = False
    try:
        config = ConfigParser()
        config.read(config_path)
        config[section][property_name] = property_value
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        time.sleep(1)
        flag = True
    except Exception as ex:
        print("Failed to change ini/properties file.", ex)
    return flag

