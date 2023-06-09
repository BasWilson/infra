import datetime
import logging

def PrintError(message):
    print(message)
    logging.error(message)

def PrintInfo(message):
    print(message)
    logging.info(message)

def SetupLogging():
    currentDate = datetime.datetime.now()
    logging.basicConfig(filename=".infra/logs/{}.log".format(datetime.datetime.isoformat(currentDate)), level=logging.INFO)