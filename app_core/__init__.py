import json
import logging
import logging.config
import os.path
import pathlib


class AppCore:
    def __init__(self, name):
        self.name = name
        self.flat_cfg = {}

    def package_directory(self):
        return os.path.abspath(os.path.dirname(__file__))

    def resource_directory(self):
        return os.path.join(self.package_directory(), "resource")

    def package_cfg_directory(self):
        return os.path.join(self.resource_directory(), "cfg")

    def package_img_directory(self):
        return os.path.join(self.resource_directory(), "img")

    def home_directory(self):
        return str(pathlib.Path.home())

    def app_directory(self):
        return os.path.join(self.home_directory(), self.name)

    def app_cfg_directory(self):
        return os.path.join(self.app_directory(), "cfg")

    def create_app_cfg_directory(self):
        os.makedirs(self.app_cfg_directory(), exist_ok=True)

    def extended_help_path(self, filename="extended.help.txt"):
        return os.path.join(self.app_directory(), filename)

    def app_log_path(self):
        return os.path.join(self.app_directory(), "log.txt")

    def read_extended_help(self):
        try:
            if os.path.exists(self.extended_help_path()):
                with open(self.extended_help_path(), "r") as h:
                    self.logger().debug(f"Reading extended help '{self.extended_help_path()}'.")
                    return h.read()
            else:
                self.logger().debug(f"Extended help file does not exists on expected path '{self.extended_help_path()}'.")
                return ""
        except Exception as e:
            self.logger().error(f"Reading extended help file from '{self.extended_help_path()}' failed")
            return ""

    def logger(self):
        return logging.getLogger(self.name)

    def set_standard_logger(self):
        os.makedirs(os.path.dirname(self.app_log_path()), exist_ok=True)
        logging.config.dictConfig(self.logger_config())

    def logger_config(self):
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'loggers': {
                f"{self.name}": {
                    'level': logging.DEBUG,
                    'propagate': False,
                    'handlers': ['console_handler', 'time_rotating_file_handler'],
                },
            },

            'handlers': {
                'console_handler': {
                    'level': logging.INFO,
                    'formatter': 'simple',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                },

                'time_rotating_file_handler': {
                    'level': logging.DEBUG,
                    'formatter': 'generic',
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'filename': self.app_log_path(),
                    'when': 'midnight',
                    'backupCount': 5
                },
            },

            'formatters': {
                'generic': {
                    'format': '%(asctime)s %(levelname)s %(message)s'
                },
                'simple': {
                    'format': '%(message)s'
                }
            },
        }

    def flat_cfg_path(self):
        return os.path.join(self.app_cfg_directory(), "flat.json")

    def create_flat_cfg(self, default_cfg):
        path = self.flat_cfg_path()
        if not os.path.exists(path):
            try:
                with open(path, "w+") as f:
                    json.dump(default_cfg, f)
                    self.logger().debug(f"Flat CFG created in path {path}")
            except Exception as e:
                self.logger().error(f"Creation of flat CFG failed. Path was {path}")

    def read_flat_cfg(self):
        try:
            with open(self.flat_cfg_path(), "r") as f:
                self.flat_cfg = json.load(f)
        except Exception as e:
            self.logger().error(f"Reading of flat CFG failed. Path was {self.flat_cfg_path()}")

