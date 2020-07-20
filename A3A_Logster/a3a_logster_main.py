import os
import jinja2
from jinja2 import Environment
# needs to be installed!
import stdiomask


_cwd = os.getcwd()


def get_username_password():
    """
    gets username and password from user input,
    password is obscured by '*' via the stdiomask module
    Returns a tuple where [0] = user_name and [1] is password
    """
    user_name = input("Please enter your Username: ")
    password = stdiomask.getpass("Please enter your Password: ")
    return (user_name, password)


def get_template(in_template='logster_script_template.py.jinja'):
    """
    gets the template as string from a file,
    filename can be specified but also defaults if not specified
    Returns the template object
    """
    with open(os.path.join(_cwd, in_template), 'r') as jinfile:
        _template_string = jinfile.read()
    return Environment(loader=jinja2.BaseLoader).from_string(_template_string)


def get_vars(in_file):
    """
    reads a csv in and splits it into a list of dictionaries.
    name of the csv is the 'in_file' argument and the file has to be in the same folder as the script
    """
    var_list = []
    with open(os.path.join(_cwd, in_file), 'r') as csvfile:
        _csv_list = csvfile.read().splitlines(False)

    for index, line in enumerate(_csv_list):
        if index != 0:
            _var_dict = {}
            Server, Category, TARGET_SERVER, Folder, Full_log, Filtered_Log = line.split(';')
            _var_dict['target_server'] = TARGET_SERVER.strip()
            _var_dict['ftp_var'] = Folder.strip()
            _var_dict['server'] = Server.strip().replace(' ', '_')
            _var_dict['category'] = Category.strip().replace(' ', '')
            _var_dict['folder'] = Full_log.replace('\\', ' /').strip().replace(' ', '_')
            _var_dict['filtered_folder'] = Filtered_Log.replace('\\', '/').strip().replace(' ', '_')

            var_list.append(_var_dict)
    return var_list


def render_scripts(in_username, in_password, in_filter_file, in_variable_dict, in_template, in_target_folder='scripts'):
    """
    creates the scripts with jinja, creates the 'in_target_folder(default='scripts')' if it does not already exists.
    the scripts name is built from the variables.
    """
    data = in_template.render(user_name=in_username, password=in_password, filter_list_path=in_filter_file, **in_variable_dict)
    folder = os.path.join(_cwd, in_target_folder)
    script_name = f"{in_variable_dict['server']}_{in_variable_dict['category']}_script.py"
    if os.path.exists(folder) is False:
        os.mkdir(folder)
    with open(os.path.join(folder, script_name), 'w') as scriptfile:
        scriptfile.write(data)


def main():
    # get username and password
    # if you don't want to have to manually input your password, then comment out the original line(76) and the import line(5) and comment in the following line(75):

    # username, password = (YOURUSERNAME, YOURPASSWORD)
    username, password = get_username_password()
    # get the template from the template file
    template = get_template()
    filter_list_path = ''
    # loop through the list of variable dictionaries from the csv
    # and create the scripts
    for var_group in get_vars('Mappe1.csv'):
        render_scripts(username, password, filter_list_path var_group, template)


# execute the main function
main()
