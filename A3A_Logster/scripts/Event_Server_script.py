from ftplib import FTP
import pathlib
import os


USERNAME = "test_user"
PASSWORD = "test_pass"
TARGET_SERVER = "antistasi.armahosts.com_2332"
LOCAL_LOG_DIR = pathlib.Path("/www/htdocs/w0170fba/antistasi.de/dev_drive/Bob_Murphy/Full_Logs")
LOCAL_FILTERED_LOGS_DIR = pathlib.Path("/www/htdocs/w0170fba/antistasi.de/dev_drive/Bob_Murphy/Antistasi_Community_Logs")


def filter_file(inputPathObj, outputPathObj):
    with inputPathObj.open("r", encoding='utf-8', errors='ignore') as input_file:
        with outputPathObj.open("w", encoding='utf-8', errors='ignore') as output_file:
            new_f = input_file.readlines()
            for line in new_f:
                if "Server: Object" not in line:
                    if "Server: Network message" not in line:
                        if "Client: Object" not in line:
                            if "Error: Object" not in line:
                                if "Setting invalid pitch" not in line:
                                    if "Client: Remote object" not in line:
                                        if "Error in expression <];testArray = testArray + [1];testArray set [_a, 1];testArray pushBack 1;}, 0, 1>" not in line:
                                            if "Error position: <set [_a, 1];testArray pushBack 1;}, 0, 1>" not in line:
                                                if "Error Type Any, expected Number" not in line:
                                                    if "Ref to nonnetwork object" not in line:
                                                        if "Message not sent - error 0, message ID" not in line:
                                                            if "NetServer: cannot find channel #" not in line:
                                                                if "NetServer: trying to send a too large non-guaranteed message" not in line:
                                                                    output_file.write(line)
            output_file.truncate()

^
download_single_server = TARGET_SERVER != ""

ftp = FTP()
ftp.connect(host="antistasi.armahosts.com", port=8821)

ftp.login(user=USERNAME, passwd=PASSWORD)

servers = [TARGET_SERVER] if download_single_server else ftp.nlst()

print(servers)

for server in servers:
    print("Downloading files from server {}".format(server))

    rptDir = LOCAL_LOG_DIR.joinpath('')
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
        filteredRptPath = filteredRptDir.joinpath(file_name)
        filter_file(rptPath, filteredRptPath)


print("logs downloaded")