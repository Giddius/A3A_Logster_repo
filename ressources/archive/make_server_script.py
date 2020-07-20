import jinja2
from jinja2 import Environment
import os

user_name = ''
password = ''

_cwd = os.getcwd()

with open(os.path.join(_cwd, 'serve_shit.py.jinja'), 'r') as jinfile:
    _template_string = jinfile.read()
template = Environment(loader=jinja2.BaseLoader).from_string(_template_string)


def get_vars(in_file):
    var_list = []
    with open(os.path.join(_cwd, in_file), 'r') as csvfile:
        _csv_list = csvfile.readlines()

    for lines in _csv_list:
        if 'Server;Category' not in lines:
            _var_dict = {}
            Server, Category, TARGET_SERVER, Folder, Full_log, Filtered_Log = lines.split(';')
            _var_dict['target_server'] = TARGET_SERVER.strip()
            _var_dict['server'] = Server.strip().replace(' ', '_')
            _var_dict['category'] = Category.strip().replace(' ', '')
            _var_dict['folder'] = Full_log.replace('\\', ' /').strip().replace(' ', '_')
            _var_dict['filtered_folder'] = Filtered_Log.replace('\\', '/').replace('\n', '').strip().replace(' ', '_')

            var_list.append(_var_dict)
    return var_list


for item in get_vars('Mappe1.csv'):

    data = template.render(target_server=item['target_server'], folder=item['folder'], filtered_folders=item['filtered_folder'], user_name=user_name, password=password)
    with open(os.path.join(_cwd, 'scripts', item['server'] + '_' + item['category'] + '_script.py'), 'w') as sfile:
        sfile.write(data)
