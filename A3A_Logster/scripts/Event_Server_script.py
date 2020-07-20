from ftplib import FTP
import pathlib
import os


USERNAME = "YOURUSERNAME"
PASSWORD = "YOURPASSWORD"
TARGET_SERVER = "antistasi.armahosts.com_2332"
LOCAL_LOG_DIR = pathlib.Path("SOMEPATH")
LOCAL_FILTERED_LOGS_DIR = pathlib.Path("SOMEPATH")


def get_filters():
    """
    gets a list of strings to filter the logs with.
    from the file 'filter_list.txt' inside the current folder
    each line is a different filter string.
    """
    with open('filter_list.txt', 'r') as filter_file:
        return filter_file.read().splitlines()

def filter_file(inputPathObj, outputPathObj):
    """
    filters out all lines that contain a string from the filter_list.txt file
    """
    with inputPathObj.open("r", encoding='utf-8', errors='ignore') as input_file:
        with outputPathObj.open("w", encoding='utf-8', errors='ignore') as output_file:
            new_f = input_file.readlines()
            for line in new_f:
                if not any(filter in line for filter in get_filters())
                    output_file.write(line)
            output_file.truncate()


download_single_server = TARGET_SERVER != ""

ftp = FTP()
ftp.connect(host="antistasi.armahosts.com", port=8821)

ftp.login(user=USERNAME, passwd=PASSWORD)

servers = [TARGET_SERVER] if download_single_server else ftp.nlst()

print(servers)

for server in servers:
    print("Downloading files from server {}".format(server))

    rptDir = LOCAL_LOG_DIR.joinpath('Eventserver/Server')
    rptDir.mkdir(parents=True, exist_ok=True)
    print(str(rptDir) + ' save location for full logs')


    filteredRptDir = LOCAL_FILTERED_LOGS_DIR.joinpath('')
    filteredRptDir.mkdir(parents=True, exist_ok=True)
    print(str(filteredRptDir) + ' save location for filtered_logs')

    ftp.cwd("/{}/ARMAHOSTS".format(server))

    localRpts = {x.name: x.stat().st_size for x in rptDir.iterdir() if x.is_file()}
    remoteRpts = {file_name: ftp.size(file_name) for file_name in ftp.nlst() if os.path.splitext(file_name)[1] == ".rpt"}

    print("Remote Rpts: {}".format(remoteRpts))

    rptsNeeded = [file_name for file_name in remoteRpts.keys() if not (file_name in localRpts) or (localRpts[file_name] != remoteRpts[file_name])]
    print("Rpts needed: {}".format(rptsNeeded))

    for file_name in rptsNeeded:
        print("Downloading {}".format(file_name))
        rptPath = rptDir.joinpath(file_name)
        with rptPath.open(mode="wb") as fp:
            ftp.retrbinary("RETR {}".format(file_name), fp.write)

        print("Filtering {}".format(file_name))
        filteredRptPath = filteredRptDir.joinpath(file_name + '.txt')
        filter_file(rptPath, filteredRptPath)


print("logs downloaded")