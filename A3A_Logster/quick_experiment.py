import configparser
import os
from pprint import pprint
import csv
from gidtools.gidfiles import QuickFile

_out = QuickFile()

csv.register_dialect('quick_dialect', delimiter=';', quoting=csv.QUOTE_NONE)
with open("D:/Dropbox/hobby/Modding/Programs/Github/My_Repos/A3A_Logster_repo/A3A_Logster/Mappe1.csv", newline='') as inputfile:
    _content = csv.DictReader(inputfile, dialect='quick_dialect')
    _row_list = [row for row in _content]

_list = []
for item in _row_list:
    _section = item['Server'].lower()
    _category = item['Category'].lower()
    _target_server = item['TARGET_SERVER']
    _ftp_cwd = item['Folder - ftp.cwd']
    _full_log_folder = item['Full log'].strip().replace(' ', '_')
    _filtered_log_folder = item['Filtered Log'].strip().replace(' ', '_')
    _folder_name = _full_log_folder.split('/')[0].strip().replace(' ', '_')
    _out.apwrite(f'[{_section}_{_category}]')
    _out.apwrite('target_server| ' + _target_server)
    _out.apwrite('ftp_cwd| ' + _ftp_cwd)
    _out.apwrite('folder_name| ' + _full_log_folder)
    _out.apwrite('\n# ---------------------------------------------------------------------------------------------- #\n')
    _list.append(f'{_section}_{_category}')


_out.apwrite('server_list| ' + ', '.join(_list))


CFG = configparser.ConfigParser(delimiters='|', allow_no_value=True)
print(CFG)
