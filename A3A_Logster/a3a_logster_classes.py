import configparser
import os


class LogsterConfigParser(configparser.ConfigParser):
    def __init__(self, cwd_path, config_file=None, auto_read=False, **kwargs):
        super().__init__(**kwargs)
        self.cwd = cwd_path
        self.config_file = config_file
        self.login_dict = {}
        self.connect_dict = {}
        self.folder_dict = {}
        self.server_set = set([])
        self.filters = []
        if self.config_file is not None and auto_read is True:
            self.read_and_assign()

    def read_and_assign(self):
        self.read(self.config_file)
        self.login_dict = self.get_login_dict()
        self.connect_dict = self.get_connect_dict()
        self.folder_dict = self.get_folder_dict()
        self.filters = self.list_from_keys_only('filter', as_set=True)
        self.server_set = self.as_list('general_server_settings', 'server_list', as_set=True)

    def as_list(self, section, key, delimiter=',', as_set=False):
        _raw = self.get(section, key).strip()
        if _raw.endswith(delimiter):
            _raw = _raw.rstrip(delimiter)
        if _raw.startswith(delimiter):
            _raw = _raw.lstrip(delimiter).strip()
        _out = _raw.replace(delimiter + ' ', delimiter).split(delimiter)
        if as_set is True:
            _out = set(_out)
        return _out

    def list_from_keys_only(self, section, as_set=True):
        _result = self.options(section)
        _out = []
        for line in _result:
            if line != '':
                _out.append(line)
        if as_set is True:
            _out = set(_out)
        return _out

    def get_login_dict(self):
        return {'user': self.get('user', 'username'), 'passwd': self.get('user', 'password')}

    def get_connect_dict(self):
        return {'host': self.get('general_server_settings', 'username'), 'port': self.get('general_server_settings', 'username')}

    def get_folder_dict(self):
        return {'unfiltered_folder_name': self.get('output', 'log_folder_name'),
                'filtered_folder_name': self.get('output', 'filtered_log_folder_name'),
                'main_save_path': os.path.join(self.cwd, self.get('output', 'main_dir'))}
