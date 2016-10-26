#!/usr/bin/python

import subprocess
import  platform


def getMemory():
    if platform.system().lower() == "darwin":
        command = "top -l 1 | head -n 10 | grep PhysMem | sed 's/, /n /g'"
        macMemory = subprocess.check_output(command, shell=True)
        macMemory = macMemory.decode("UTF-8")
        return macMemory
    elif platform.system().lower() == "linux":
        return None
    elif platform.system().lower() == "windows":
        return None