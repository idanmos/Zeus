#!/usr/bin/python

import platform
import sys
import time
import ctypes
import subprocess
import psutil

from Providers import DeviceIDGenerator

class DeviceInfoProvider():

    def getDeviceInfo(self):
        deviceInfo = {}

        # Type of OS + Version
        if platform.system().lower() == "darwin":
            deviceInfo["os"] = "Mac OS X"
        elif platform.system().lower() == "linux":
            deviceInfo["os"] = "Linux"
        elif platform.system().lower() == "windows":
            deviceInfo["os"] = "Windows"

            deviceInfo["release"] = platform.release()

        # 32/64 bit
        if sys.maxsize > 2**32:
            deviceInfo["cpuArchitecture"] = "64"
        else:
            deviceInfo["cpuArchitecture"] = "32"

        # List of installed applications
        deviceInfo["installedApps"] = "None"
        #if platform.system().lower() == "darwin":
            #installedApps = subprocess.check_output(['ls', '-l', '/Applications']).splitlines()
            #deviceInfo["installedApps"] = installedApps

        # RAM (used and installed)
        totalMemory = psutil.virtual_memory().total
        availableMemory = psutil.virtual_memory().available

        totalMemory = "%.2f" % (totalMemory / 1024 / 1024 / 1024)
        availableMemory = "%.2f" % (availableMemory/1024/1024/1024)

        if totalMemory and availableMemory:
            memory = "{%s|%s}" % (totalMemory, availableMemory)
            deviceInfo["memory"] = memory

        # Local Date & Time
        deviceInfo["time"] = time.strftime("%H:%M:%S")
        deviceInfo["date"] = time.strftime("%d/%m/%Y")

        # Device ID
        deviceIdGen = DeviceIDGenerator.generateDeviceID()
        deviceInfo["deviceID"] = deviceIdGen

        return deviceInfo


    def getClipboardData(self):
        clipboardData = None

        if platform.system().lower() == "windows":
            import ctypes

            CF_TEXT = 1

            kernel32 = ctypes.windll.kernel32
            user32 = ctypes.windll.user32

            user32.OpenClipboard(0)
            if user32.IsClipboardFormatAvailable(CF_TEXT):
                data = user32.GetClipboardData(CF_TEXT)
                data_locked = kernel32.GlobalLock(data)
                text = ctypes.c_char_p(data_locked)
                kernel32.GlobalUnlock(data_locked)

                clipboardData = text.value
            else:
                user32.CloseClipboard()
        elif platform.system().lower() == "darwin":
            import subprocess

            clipboardData = subprocess.check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')
        elif platform.system().lower() == "linux":
            pass

        return clipboardData

if __name__ == "__main__":
    print("[i] Device information:\n------\n%s" % DeviceInfoProvider().getDeviceInfo())