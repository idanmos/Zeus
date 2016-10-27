import platform

# TODO: Windows

def getHardDiskSerialNumber():
    if platform.system().lower() == "linux": # TODO: Check if it works
        import ctypes
        from ctypes.util import find_library
        from ctypes import Structure

        class DBusError(Structure):
            _fields_ = [("name", ctypes.c_char_p),
                        ("message", ctypes.c_char_p),
                        ("dummy1", ctypes.c_int),
                        ("dummy2", ctypes.c_int),
                        ("dummy3", ctypes.c_int),
                        ("dummy4", ctypes.c_int),
                        ("dummy5", ctypes.c_int),
                        ("padding1", ctypes.c_void_p), ]

        class HardwareUuid(object):

            def __init__(self, dbus_error=DBusError):
                self._hal = ctypes.cdll.LoadLibrary(find_library('hal'))
                self._ctx = self._hal.libhal_ctx_new()
                self._dbus_error = dbus_error()
                self._hal.dbus_error_init(ctypes.byref(self._dbus_error))
                self._conn = self._hal.dbus_bus_get(ctypes.c_int(1),
                                                    ctypes.byref(self._dbus_error))
                self._hal.libhal_ctx_set_dbus_connection(self._ctx, self._conn)
                self._uuid_ = None

            def __call__(self):
                return self._uuid

            @property
            def _uuid(self):
                if not self._uuid_:
                    udi = ctypes.c_char_p("/org/freedesktop/Hal/devices/computer")
                    key = ctypes.c_char_p("system.hardware.uuid")
                    self._hal.libhal_device_get_property_string.restype = \
                        ctypes.c_char_p
                    self._uuid_ = self._hal.libhal_device_get_property_string(
                        self._ctx, udi, key, self._dbus_error)
                return self._uuid_

        get_uuid = HardwareUuid()

        return get_uuid()
    elif platform.system().lower() == "darwin":
        import subprocess

        results = subprocess.check_output(
            "/usr/sbin/system_profiler SPHardwareDataType | fgrep 'Serial' | awk '{print $NF}'",
            shell=True)
        if not results:
            results = subprocess.check_output("ioreg -l | awk '/IOPlatformSerialNumber/ { print $4 }' | sed s/\"//g",
                                              shell=True)

        if results:
            results = results.decode("UTF-8")

            return results
    elif platform.system().lower() == "windows":
        import subprocess
        import os

        windowsDrive = os.environ["homedrive"]
        command = r"vol %s" % windowsDrive
        commandOutput = subprocess.check_output(command, shell=True).decode("UTF-8").split(" ")
        results = commandOutput[-1]

        return results

def getComputerName():
    computerName = platform.node()
    return computerName

def generateDeviceID():
    deviceID = r"{%s|%s}" % (getComputerName(), getHardDiskSerialNumber())
    deviceID = deviceID.replace("\n", "")
    deviceID = deviceID.replace("\r", "")
    return deviceID