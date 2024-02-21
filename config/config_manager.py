import configparser
import os
import platform

from globals.dir_global import INI_CONFIGS_PATH


class ConfigManager:

    if platform.system() == 'Windows':
        __PATH_TO_CONFIG_FILES = "\\config\\"
    else:
        __PATH_TO_CONFIG_FILES = "/config/"

    def __init__(self, ini_file):
        self.file_path = os.path.join(INI_CONFIGS_PATH, ini_file)
        self.config = configparser.ConfigParser()
        self.config.read(self.file_path)

    def _get_property(self, section, key):
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            raise Exception(f"Error: {e}")

    @property
    def login_url(self):
        return self._get_property('test_info', "login_url")

    @property
    def user_name(self):
        return self._get_property('test_info', "user_name")

    @property
    def user_password(self):
        return self._get_property('test_info', "user_password")

    @property
    def firm(self):
        return self._get_property('test_info', "firm")
