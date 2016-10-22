class TaskManagmentHandler(self):
    # Handle tasks from server

    MINUTES_TO_FIRST_TASK = 5
    MINUTES_TO_NORMAL_TASK = 20
    MINUTES_TO_FAILED_TASK = 20


    def startNewTask():
        thread = Thread(target=executeTaskFromServer, args=())
        thread.start()


    def executeTaskFromServer():
        taskResponse = urllib.request.urlopen("http://192.168.0.102/control.php?task=getTask&agent=zeus").read()

    # start normal task after 5 minutes
    # start cycled task every 20 minutes (task call itself after 20 minutes)