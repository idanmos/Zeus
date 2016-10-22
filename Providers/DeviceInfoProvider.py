class DeviceInfoProvider(object):
    def getDeviceInfo(self):
        if platform.system().lower() == "Darwin".lower():
            print("OS: Mac OS X")
        elif platform.system().lower() == "Linux".lower():
            print("OS: Linux")
        elif platform.system().lower() == "Windows".lower():
            print("OS: Windows")
