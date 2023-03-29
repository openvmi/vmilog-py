from fileinput import filename
import logging
import logging.handlers
from pathlib import Path
import enum

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

class LogLevelEnum(enum.Enum):
    critical = logging.CRITICAL
    fatal = logging.FATAL
    error = logging.ERROR
    warning = logging.WARNING
    info = logging.INFO
    debug = logging.DEBUG
    notset = logging.NOTSET

class _logLevel:
    g_logLevel = None

def setLoggerLevel(level=LogLevelEnum.warning):
    _logLevel.g_logLevel = level

def getLogger(logName='default_vmilabs', savedPath=".",enableFile=False, enableConsole=False, logLevel=None):
    if logName == "":
        logName = 'default_vmilabs'
    if logLevel is None:
        logLevel = _logLevel.g_logLevel if _logLevel.g_logLevel is not None else LogLevelEnum.warning
    logLevel = logLevel.value
    p = Path(savedPath)
    if p.is_file():
        p = p.parent
    elif p.is_dir():
        pass
    elif p.exists() is False:
        p.mkdir(parents=True, exist_ok=True)
    _logger = logging.getLogger(logName)
    _logger.setLevel(logLevel)
    _logFileName = p / (logName + ".log")
    if enableFile is True:
        handler = logging.handlers.RotatingFileHandler(
            _logFileName,
            maxBytes= 50 * 1024 * 1023,
            backupCount=10
        )
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)s]: %(message)s"
        formatter = logging.Formatter(FORMAT)
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
    
    if enableConsole is True:
        consoleHandler = logging.StreamHandler()
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)s]: %(message)s"
        formatter = logging.Formatter(FORMAT)
        consoleHandler.setFormatter(formatter)
        _logger.addHandler(consoleHandler)
    return _logger

class vmilog:
    def __init__(self, loggerName):
        self._loggerName = loggerName
        self._logger = logging.getLogger(loggerName)
        self._logger.addHandler(NullHandler())

    def enableFileHandler(self, handler=None, fileName=None):
        _logFileName = fileName
        if _logFileName is None:
            _logFileName = self._loggerName + "_d.log"
        if handler is None:
            handler = logging.handlers.RotatingFileHandler(
                _logFileName,
                maxBytes=50 * 1024 * 1024,
                backupCount= 10,
            )
            FORMAT = "[%(filename)s:%(lineno)s - %(funcName)s]: %(message)s"
            formatter = logging.Formatter(FORMAT)
            handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def enableConsoleHandler(self, handler=None):
        if handler is None:
            handler = logging.StreamHandler()
            FORMAT = "[%(filename)s:%(lineno)s - %(funcName)s]: %(message)s"
            formatter = logging.Formatter(FORMAT)
            handler.setFormatter(formatter)
        self._logger.addHandler(handler)
    
    def error(self,msg):
        self._logger.error(msg)
    
    def warning(self, msg):
        self._logger.warning(msg)
    
    def debug(self, msg):
        self._logger.debug(msg)
    
    def info(self, msg):
        self._logger.info(msg)
    
    def setLogLevel(self, level):
        obj = {
            "critical": logging.CRITICAL,
            "error": logging.ERROR,
            "warning": logging.WARNING,
            "info": logging.INFO,
            "debug": logging.DEBUG,
            "notset": logging.NOTSET
        }
        lowcaseLevel = level.lower()
        logLevel = obj.get(lowcaseLevel, logging.WARNING)
        self._logger.setLevel(logLevel)

_logger = vmilog(loggerName="default_vmilog")

def enableFileHandler(handler=None, fileName=None):
    _logger.enableFileHandler(handler=handler, fileName=fileName)

def enableConsoleHandler(handler=None):
    _logger.enableConsoleHandler(handler=handler)

def error(msg):
    _logger.error(msg)

def warning(msg):
    _logger.warning(msg)

def debug(msg):
    _logger.debug(msg)

def info(msg):
    _logger.info(msg)

def setLogLevel(level):
    _logger.setLogLevel(level=level)



