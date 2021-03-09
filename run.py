import requests
import sys
import traceback
import m3u8dler
import logger

printer = logger.CLIPrinter()

printer.print("### run.py","i")
if len(sys.argv)<=2:#判断有没有链接或路劲
    #print("Please add a download link or path after the script.")
    printer.print("Please add a download link or path after the script.","i")
else:
    varType = sys.argv[1]
    url = sys.argv[2]
    m3u8dler.preProcess(varType, url, printer, m3u8dler.cliInputAndDownload)


