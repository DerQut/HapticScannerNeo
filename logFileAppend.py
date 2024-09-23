import os
from time import gmtime, strftime


def logFileAppend(fileName: str, message: str):
    """
    Append a message to the end of a given log file with a datetime stamp
    :param fileName: Directory of the log file
    :param message: Message to be appended
    :return: None
    """

    if not os.path.exists(fileName):
        open(fileName, "w+").close()

    logFile = open(fileName, "a")
    logFile.write(f"[{strftime("%Y-%m-%d %H:%M:%S", gmtime())}] {message}\n")
    logFile.close()
