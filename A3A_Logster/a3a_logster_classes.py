import configparser
import os
import logging
from logging import handlers


def log_folderer(in_log_file_name, in_main_log_folder='logs', in_old_log_subfolder='old_logs'):
    _cwd = os.getcwd()
    _path_to_old_folder = f"{_cwd}/{in_main_log_folder}/{in_old_log_subfolder}"
    if os.path.exists(_path_to_old_folder) is False:
        os.makedirs(_path_to_old_folder)
    return f"{_cwd}/{in_main_log_folder}/{in_log_file_name}.log"


def std_namer(name):
    _nameparts = name.split('.')
    _path, _basename = _nameparts[0].rsplit('\\', 1)
    return f'{_path}/old_logs/{_basename}_{_nameparts[2]}.{_nameparts[1]}'


def main_logger(in_file_name, in_level, in_back_up=2):

    _out = logging.getLogger('main')
    _out.setLevel(getattr(logging, in_level.upper()))
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(lineno)s : %(funcName)s : %(message)s')
    should_roll_over = os.path.isfile(in_file_name)
    handler = handlers.RotatingFileHandler(in_file_name, mode='a', backupCount=in_back_up)
    handler.namer = std_namer
    if should_roll_over:
        handler.doRollover()
    handler.setFormatter(formatter)
    _out.addHandler(handler)

    return _out


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
