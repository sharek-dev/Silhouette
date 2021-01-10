import os
import sys
import configparser
import click

class ApplicationConfig:
    def __init__(self, settings_file):
        self.config = self.get_parser(settings_file)

    def get_parser(self, path):
        parser = configparser.ConfigParser()
        parser.read(path)
        return parser

    def get_config(self, section, key):
        return self.config.get(section, key, vars=os.environ)

    def get_section_keys(self, section):
        return list(self.config[section].keys())

    def get_vars(self):
        return { key: self.get_config("VARS", key) for key in self.get_section_keys("VARS")  }

    def get_str(self, section, key):
        return str(self.get_config(section, key))

    def get_int(self, section, key):
        return int(self.get_config(section, key))

    def get_list(self, section, key, sep=","):
        return str(self.get_config(section, key)).split(sep)