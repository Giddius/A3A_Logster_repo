import time
import subprocess

# full path to each script as a string into this list
SCRIPT_LIST = ['D:/Dropbox/hobby/Modding/Programs/Github/My_Repos/A3A_Logster_repo/A3A_Logster/quick_experiment.py']

# how long to wait in between in minutes
WAIT_MIN = 1

# ignore this, just so the loop keeps going
RUN = 1


def min_to_sec(minutes: int):
    return round(minutes * 60)


while RUN == 1:
    for script in SCRIPT_LIST:
        subprocess.run(['sudo', '-u www-data', 'php', 'occ', 'files:scan', '--all'], check=False, shell=True)

    time.sleep(min_to_sec(WAIT_MIN))
