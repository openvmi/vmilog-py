if __name__ == "__main__":
    import _logging
    _logging.setLogLevel("info")
    _logging.enableConsoleHandler()
    _logging.enableFileHandler(fileName="mylog.go")
    _logging.info("hello, info")
    _logging.warning("hello, warning")
    _logging.debug("hello, debug")