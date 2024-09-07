import logging

# ---- New Logging Process ----
def newloggingfunction(BOTName, rundate):
    
    global print
    global LogFilePath

    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger()
    LogFilePath = "log\\" + str(BOTName) + "_" + str(rundate) + "_log.txt"
    logger.addHandler(logging.FileHandler(LogFilePath, "a"))
    print = logger.info
    return (logger.info)