#!/usr/bin/python

import platform
import sys
import time
import ctypes
import  DeviceIDGenerator

def ram():
    kernel32 = ctypes.windll.kernel32
    c_ulong = ctypes.c_ulong

    class MEMORYSTATUS(ctypes.Structure):
        _fields_ = [
            ('dwLength', c_ulong),
            ('dwMemoryLoad', c_ulong),
            ('dwTotalPhys', c_ulong),
            ('dwAvailPhys', c_ulong),
            ('dwTotalPageFile', c_ulong),
            ('dwAvailPageFile', c_ulong),
            ('dwTotalVirtual', c_ulong),
            ('dwAvailVirtual', c_ulong)
        ]

    memoryStatus = MEMORYSTATUS()
    memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
    kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))
    mem = memoryStatus.dwTotalPhys / (1024 * 1024)
    availRam = memoryStatus.dwAvailPhys / (1024 * 1024)
    if mem >= 1000:
        mem = mem / 1000
        totalRam = str(mem) + ' GB'
    else:
        #        mem = mem/1000000
        totalRam = str(mem) + ' MB'
    return (totalRam, availRam)

class DeviceInfoProvider:

    global deviceInfo
    deviceInfo = {}

    def getDeviceInfo():
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
        installedApps = []
        #deviceInfo["installedApps"] = getInstalledApps()

        # RAM (used and installed)

        # Local Date & Time
        deviceInfo["time"] = time.strftime("%H:%M:%S")
        deviceInfo["date"] = time.strftime("%d/%m/%Y")

        # Device ID
        deviceIdGen = DeviceIDGenerator.generateDeviceID()
        deviceInfo["deviceID"] = deviceIdGen


    getDeviceInfo()
    print("Device info: %s" % deviceInfo)
    #print("RAM: %s" % ram())