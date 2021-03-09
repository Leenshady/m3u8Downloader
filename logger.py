import logging
import os
import os.path
from pathlib import Path
import time

class Printer(object):
    #打印类
    def print(self,info):
        pass

class LogPrinter(Printer):
    #日志打印类
    def __init__(self):
        # 第一步，创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)  # Log等级总开关

        logFilePath = Path("log/")
        if logFilePath.exists()==False:
            os.mkdir(logFilePath)
        
        log_path = os.getcwd() + '\\log\\'
        log_name = log_path + 'log.log'
        logfile = log_name

        fh = logging.FileHandler(logfile, mode='w')
        fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

        # 第三步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)

        # 第四步，将logger添加到handler里面
        logger.addHandler(fh)
        self.logger = logger

    def print(self,msg,type):
        if(type=="i"):
            self.logger.info(msg)
        elif(type=="w"):
            self.logger.warning(msg)
        elif(type=="e"):
            self.logger.error(msg)
        elif(type=="d"):
            self.logger.debug(msg)
        else:
            self.logger.info(msg)

class CLIPrinter(Printer):
    #命令行打印类
    def print(self,msg,type):
        if(type=="i"):
            print("INFO: "+msg)
        elif(type=="w"):
            print("WARNING: "+msg)
        elif(type=="e"):
            print("ERROR: "+msg)
        elif(type=="d"):
            print("DEBUG: "+msg)
        else:
            print("INFO: "+msg)

