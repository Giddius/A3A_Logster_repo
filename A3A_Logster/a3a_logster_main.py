# region [Imports]

import os
import sys
from ftplib import Error, FTP

from a3a_logster_classes import LogsterConfigParser, log_folderer, main_logger

# endregion [Imports]

# region [Logging]

pylog = main_logger(log_folderer('a3a_logster_log', in_main_log_folder='python_script_logs', in_old_log_subfolder='old_python_script_logs'), 'info', 5)
pylog.info("# " + "*-$-" * 6 + "* --> NEW_RUN <-- " + "*-?-" * 6 + "* #")

# endregion [Logging]

# region [Paths]

CWD_PATH = os.getcwd()
CFG_PATH = os.path.join(CWD_PATH, 'a3a_logster_config.ini')

# endregion [Paths]

# region [Constants]


# endregion [Constants]

# region [Global_Functions]

def create_folders(in_folder):
    if os.path.isdir(in_folder) is False:
        pylog.debug('Folder %s does not exist, creating it now', in_folder)
        os.makedirs(in_folder)
        pylog.info('Folder %s was created', in_folder)
    else:
        pylog.debug('Folder %s already existing, does not need to be created', in_folder)


def create_folders_from_list(in_list):
    for folder in in_list:
        pylog.debug('folder input list: %s', ', '.join(in_list))
        create_folders(folder)

# endregion [Global_Functions]

# region [Factories]


class LogDownloader:
    def __init__(self, name, cfg_holder, ftp_object):
        pylog.info('starting initiation of %s instance with the name: %s', self.__class__, name)
        self.name = name
        self.cfg_holder = cfg_holder
        self.ftpcon = ftp_object
        self.new_logs = []
        self.log_folder, self.filtered_log_folder = self.create_folder()
        pylog.info('initiation of %s instance with name: %s completed', self.__class__, name)
        self.download_logs()

    def create_folder(self):
        pylog.debug('Class: %s, Name: %s -- starting process of checking and creating folders', self.__class__, self.name)
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
        pylog.debug('%s local logs were found in %s', len(_out), self.log_folder)
        return _out

    @property
    def remote_logs(self):
        _out = {}
        for filename in self.ftpcon.nlst():
            if filename.endswith('.rpt'):
                _out[filename] = self.ftpcon.size(filename)
        pylog.debug('%s remote logs were found in %s', len(_out), f"/{self.cfg_holder.get(self.name, 'target_server')}/{self.cfg_holder.get(self.name, 'ftp_cwd')}")
        return _out

    def download_logs(self):
        self.ftpcon.cwd(f"/{self.cfg_holder.get(self.name, 'target_server')}/{self.cfg_holder.get(self.name, 'ftp_cwd')}")
        pylog.debug('changed ftp cwd to: %s', f"/{self.cfg_holder.get(self.name, 'target_server')}/{self.cfg_holder.get(self.name, 'ftp_cwd')}")
        pylog.info('Class: %s, Name: %s -- starting process of donwloading new logs', self.__class__, self.name)
        _local_logs = self.local_logs
        _remote_logs = self.remote_logs
        for filename in _remote_logs:
            if filename not in _local_logs or _remote_logs[filename] != _remote_logs[filename]:
                self._log_downloader(filename)
        pylog.debug('%s new logs downloaded', len(self.new_logs))

    def _log_downloader(self, filename):
        _download_path = os.path.join(self.log_folder, filename)
        with open(_download_path, 'wb') as remfile:
            self.ftpcon.retrbinary(f"RETR {remfile}", remfile.write)
        self.new_logs.append((filename, _download_path))

    def filter_logs(self):
        pylog.info('Class: %s, Name: %s -- starting process of filtering new logs', self.__class__, self.name)
        for filename, filepath in self.new_logs:
            _filtered_path = os.path.join(self.filtered_log_folder, filename.split('.')[0] + '.txt')
            _content_list = []
            with open(filepath, "r", encoding='utf-8', errors='ignore') as input_file:
                for line in input_file.read().splitlines():
                    if all(filter not in line for filter in self.cfg_holder.filters):
                        _content_list.append(line)
            with open(_filtered_path, "w", encoding='utf-8', errors='ignore') as output_file:
                output_file.write('\n'.join(_content_list))
        for files in os.listdir(self.filtered_log_folder):
            if files.endswith('.rpt'):
                try:
                    os.rename(os.path.join(self.filtered_log_folder, files), os.path.join(self.filtered_log_folder, files.split('.')[0] + '.txt'))
                except Error as e:
                    pylog.critical('could not rename file %s, because: %s', os.path.join(self.filtered_log_folder, files), e)


class LogDownloadFactory:
    CFG_PATH = os.path.join(CWD_PATH, 'a3a_logster_config.ini')
    cfg_holder = LogsterConfigParser(cwd_path=CWD_PATH, config_file=CFG_PATH, auto_read=True, delimiters='|', allow_no_value=True)

    def __init__(self, filter_files=True):
        pylog.info('starting initiation of %s instance', self.__class__)
        self.ftp = FTP()
        self.ftp_status = 'closed'
        self.downloaders = {}
        self.filter_files = filter_files

    def open_connection(self):
        if self.ftp_status != 'open' and self.ftp_status != 'quited':
            pylog.info('opening ftp connection')
            self.ftp.connect(**self.cfg_holder.connect_dict)
            self.ftp.login(**self.cfg_holder.login_dict)
            _welcome = self.ftp.getwelcome()
            print(_welcome)
            pylog.info('ftp connection established\n\n%s', _welcome)
            self.ftp_status = 'open'
        elif self.ftp_status == 'open':
            pylog.warning('connection is already open!')
        elif self.ftp_status == 'quited':
            pylog.critical('connection was already closed prior, cannot be reopen in this script run')

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
        if self.filter_files is True:
            self.filter_all()

    def filter_all(self):
        for _, value in self.downloaders.items():
            value.filter_logs()

# endregion [Factories]


def main(filter_logs: bool, excluded):
    log_getter = LogDownloadFactory(filter_files=filter_logs)
    log_getter.create_all(exclude=excluded)
    print('All Processes completed!')


# region [Main_Exec]
if __name__ == '__main__':
    FILTER_FILES = False if len(sys.argv) > 1 and sys.argv[1] == '-nf' else True
    if len(sys.argv) > 2:
        EXCLUDED_LIST = [
            excluded for index, excluded in sys.argv if index not in [1, 2]
        ]

    else:
        EXCLUDED_LIST = None
    pylog.info('Filter_files was detected as %s, Exclude List as: %s', FILTER_FILES, str((EXCLUDED_LIST)))
    main(FILTER_FILES, EXCLUDED_LIST)


# endregion [Main_Exec]
