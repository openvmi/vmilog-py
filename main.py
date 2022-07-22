if __name__ == "__main__":
    import vmilog
    vmilog.setLogLevel("info")
    vmilog.enableConsoleHandler()
    vmilog.enableFileHandler(fileName="mylog.go")
    vmilog.info("hello, info")
    vmilog.warning("hello, warning")
    vmilog.debug("hello, debug")