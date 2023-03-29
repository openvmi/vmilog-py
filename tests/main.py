import sys

sys.path.append('../src')

from vmilog import setLoggerLevel, vmilog, LogLevelEnum, getLogger
import logging

myLogger = vmilog('mynewLogger')
myLogger.enableConsoleHandler()
myLogger.enableFileHandler()
myLogger.setLogLevel('info')
def myfun():
    log = getLogger(enableFile=True, logLevel =LogLevelEnum.info)
    log.warning("hello, world")
if __name__ == "__main__":
    setLoggerLevel(LogLevelEnum.info)
    myLogger.info('hello, info')
    myfun()
    log2 = getLogger(logName="logmain", enableFile=True, enableConsole=True, logLevel=LogLevelEnum.debug)
    log2.debug("hello, from log2")
    # _logging.setLogLevel("info")
    # _logging.enableConsoleHandler()
    # _logging.enableFileHandler(fileName="mylog.go")
    # _logging.info("hello, info")
    # _logging.warning("hello, warning")
    # _logging.debug("hello, debug")