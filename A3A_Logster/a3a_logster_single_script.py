# region [Imports]

from ftplib import FTP
import os
from a3a_logster_classes import LogsterConfigParser

# endregion [Imports]

# region [Paths]

CWD_PATH = os.getcwd()

# endregion [Paths]

# region [Support_Objects]


# endregion [Support_Objects]

# region [Constants]


# endregion [Constants]

# region [Global_Functions]

def create_folders(in_folder):
    if os.path.isdir(in_folder) is False:
        os.makedirs(in_folder)


def create_folders_from_list(in_list):
    for folder in in_list:
        create_folders(folder)

# endregion [Global_Functions]

# region [Factories]


class LogDownloader:
    def __init__(self, name, cfg_holder, ftp_object):
        self.name = name
        self.cfg_holder = cfg_holder
        self.ftpcon = ftp_object
        self.new_logs = []
        self.log_folder, self.filtered_log_folder = self.create_folder()
        self.download_logs()

    def create_folder(self):
        _main_folder = self.cfg_holder.folder_dict.get('main_save_path')
        _server_folder = os.path.join(_main_folder, self.cfg_holder.get(self.name, 'folder_name'))
        _log_folder = os.path.join(_server_folder, self.cfg_holder.folder_dict.get('unfiltered_folder_name'))
        _filtered_log_folder = os.path.join(_server_folder, self.cfg_holder.folder_dict.get('filtered_folder_name'))
        create_folders_from_list([_main_folder, _server_folder, _log_folder, _filtered_log_folder])
        return (_log_folder, _filtered_log_folder)

    @property
    def local_logs(self):
        _out = {}
        for filename in os.listdir(self.log_folder):
            if filename.endswith('.rpt'):
                _out[filename] = os.stat(os.path.join(self.log_folder, filename)).st_size
        return _out

    @property
    def remote_logs(self):
        _out = {}
        for filename in self.ftpcon.nlst():
            if filename.endswith('.rpt'):
                _out[filename] = self.ftpcon.size(filename)
        return _out

    def download_logs(self):
        self.ftpcon.cwd(f"/{self.cfg_holder.get(self.name, 'target_server')}/{self.cfg_holder.get(self.name, 'ftp_cwd')}")
        _local_logs = self.local_logs
        _remote_logs = self.remote_logs
        for filename in _remote_logs:
            if filename not in _local_logs or _remote_logs[filename] != _remote_logs[filename]:
                self._log_downloader(filename)

    def _log_downloader(self, filename):
        _download_path = os.path.join(self.log_folder, filename)
        with open(_download_path, 'wb') as remfile:
            self.ftpcon.retrbinary(f"RETR {remfile}", remfile.write)
        self.new_logs.append((filename, _download_path))

    def filter_logs(self):
        for filename, filepath in self.new_logs:
            _filtered_path = os.path.join(self.filtered_log_folder, filename)
            with open(filepath, "r", encoding='utf-8', errors='ignore') as input_file:
                with open(_filtered_path, "a", encoding='utf-8', errors='ignore') as output_file:
                    for line in input_file.read().splitlines():
                        if all(filter not in line for filter in self.cfg_holder.filters):
                            output_file.write(line + '\n')


class LogDownloadFactory:
    CFG_PATH = CWD_PATH.joinpath('config', 'a3a_logster_config.ini')
    cfg_holder = LogsterConfigParser(cwd_path=CWD_PATH, config_file=CFG_PATH, auto_read=True, delimiters='|', allow_no_value=True)

    def __init__(self, filter_files=True):
        self.ftp = FTP()
        self.ftp_status = 'closed'
        self.downloaders = {}
        self.filter_files = filter_files

    def open_connection(self):
        if self.ftp_status != 'open' and self.ftp_status != 'quited':
            self.ftp.connect(**self.cfg_holder.connect_dict)
            self.ftp.login(**self.cfg_holder.login_dict)
            print(self.ftp.getwelcome())
            self.ftp_status = 'open'

    def create_all(self, exclude=None):
        _exclude = [] if exclude is None else exclude
        if self.ftp_status == 'closed':
            self.open_connection()
        if self.ftp_status == 'open':
            for server in self.cfg_holder.server_set:
                if server not in _exclude and server not in self.downloaders:
                    self.downloaders[server] = LogDownloader(server, self.cfg_holder, self.ftp)
            self.ftp.quit()
            self.ftp_status = 'quited'


# endregion [Factories]


def main():
    pass


# region [Main_Exec]

if __name__ == '__main__':
    pass


# endregion [Main_Exec]
