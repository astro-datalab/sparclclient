# Python Standard Library
import configparser
import os.path


class Conf():
    """
    Configuration parameters for `ada_client`.
    """

    def __init__(self, conf_file=None):
        config = configparser.ConfigParser()
        conf_files = ['~/sparc.ini', 'sparcl/sparc.ini']
        if conf_file is None:
            for cf in conf_files:
                if os.path.exists(os.path.expanduser(cf)):
                    config.read(os.path.expanduser(cf))

        if 'ada.server' not in config:
            raise Exception(f'Could not find conf file in any of: '
                            f'{(",").join(conf_files)} '
                            f'Create one and try again.'
                            )

        self.config = config

    @property
    def server_baseurl(self):
        return self.config['sparc.server']['ServerBaseUrl']

    @property
    def server_timeout(self):
        return self.config['sparc.server']['ServerTimout']
