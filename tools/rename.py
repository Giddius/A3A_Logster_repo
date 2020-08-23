"""
Renames all .pt files to .rpt.txt files recursively

Returns
-------
None
"""

import os


_cwd = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\A3A_Logster_repo\A3A_Logster".replace('\\', '/')


# -------------------------------------------------------------- file_walker -------------------------------------------------------------- #
def file_walker(in_path):
    # -------------------------------------------------------------- file_walker -------------------------------------------------------------- #
    """
    walks recursively through a file system and returns a list of file paths.

    Parameters
    ----------
    in_path : str
        the path to the directory from where to start

    Returns
    -------
    list
        a list of all files found as file paths.
    """
    _out_list = []

    for root, _, filelist in os.walk(in_path):
        for files in filelist:
            _out = os.path.join(root, files)
            _out_list.append(_out)

    return _out_list


for files in file_walker(_cwd):

    if 'Antistasi_Community_Logs'.lower() in files.lower() and files.endswith('.rpt'):
        if os.path.exists(files + '.txt') is True:
            os.remove(files + '.txt')
            print(f"deleted and overwriting [{files}]")
        os.rename(files, files + '.txt')
