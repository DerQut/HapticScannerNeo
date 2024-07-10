import os
from time import gmtime, strftime


def logFileAppend(fileName: str, message: str):

    if not os.path.exists(fileName):
        open(fileName, "w+").close()

    logFile = open(fileName, "a")
    logFile.write(f"[{strftime("%Y-%m-%d %H:%M:%S", gmtime())}] {message}\n")
    logFile.close()
