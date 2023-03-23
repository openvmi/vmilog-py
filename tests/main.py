import sys

sys.path.append('../src')

from vmilog import *
import logging

myLogger = vmilog('mynewLogger')
myLogger.enableConsoleHandler()
myLogger.enableFileHandler()
myLogger.setLogLevel('info')
def myfun():
    log = getLogger(enableFile=True, logLevel =logging.INFO)
    log.warning("hello, world")
if __name__ == "__main__":
    myLogger.info('hello, info')
    myfun()
    # _logging.setLogLevel("info")
    # _logging.enableConsoleHandler()
    # _logging.enableFileHandler(fileName="mylog.go")
    # _logging.info("hello, info")
    # _logging.warning("hello, warning")
    # _logging.debug("hello, debug")