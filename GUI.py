import tkinter as tk
import os
import m3u8dler
import logger
import time
import tkinter.messagebox as messagebox

option = ""
progressBarGUIFlag = True

def progressBarGUI():
    pgb = tk.Tk()
    pgb.title("m3u8Downloader -https://github.com/Leenshady/m3u8Downloader")

    sw = pgb.winfo_screenwidth()
    sh = pgb.winfo_screenheight()
    ww = 200
    wh = 180
    x = (sw-ww) / 2
    y = (sh-wh) / 2 - 10
    pgb.geometry("%dx%d+%d+%d" %(ww,wh,x,y))

    pgb.minsize(ww, wh)
    pgb.maxsize(ww, wh)

    v = tk.StringVar(master=pgb)
    tk.Label(pgb, text='下载进度:', ).place(x=20, y=30)
    progress = tk.Label(pgb, textvariable=v)
    v.set('0%')
    progress.place(x=110, y=30)
    button = tk.Button(pgb,text="取消下载", command=lambda:stopDownload(pgb))
    button.place(x=70,y=90)
    global progressBarGUIFlag
    while(int(m3u8dler.progressValue)!=1 and progressBarGUIFlag == True):
        v.set(str(m3u8dler.progressValue*100)[0:5]+"%")
        pgb.update()
        time.sleep(0.02)
    v.set('下载完成！')
    pgb.mainloop()

def stopDownload(pgb):
    m3u8dler.isStop = True
    messagebox.showinfo('提示','已取消下载')
    global progressBarGUIFlag
    progressBarGUIFlag = False
    pgb.destroy()
    main()

def masterPlaylistOptGUI(info,protocol,host,url,downloadUrl):
    mpog = tk.Tk()
    mpog.title("m3u8Downloader -https://github.com/Leenshady/m3u8Downloader")

    sw = mpog.winfo_screenwidth()
    sh = mpog.winfo_screenheight()
    ww = 700
    wh = 180
    x = (sw-ww) / 2
    y = (sh-wh) / 2 - 10
    mpog.geometry("%dx%d+%d+%d" %(ww,wh,x,y))

    mpog.minsize(ww, wh)
    mpog.maxsize(1000, wh)

    #这里是个巨坑，master参数一定要填上，不然radio不会绑定到Radiobutton上
    radio = tk.IntVar(master=mpog)
    r = []
    for i in range(len(info)):
        m3u8dler.printer.print("###GUI.py p i="+str(i),"i")
        r.append(tk.Radiobutton(mpog, text=info[i], variable=radio, value=i))
        r[i].pack(side=tk.TOP, expand=tk.YES, fill=tk.Y)
        r[i].select()
    button = tk.Button(mpog,text="下载", command=lambda:m3u8dler.thread_download(protocol,host,url,downloadUrl,radio.get(),mpog))
    button.pack(side=tk.TOP, expand=tk.YES, fill=tk.Y)
    mpog.mainloop()
    return

def download(url,root):
    root.destroy()
    m3u8dler.preProcess(option,url,logger.LogPrinter(),masterPlaylistOptGUI)

def selectF():
    global option
    option="-f"

def selectU():
    global option
    option="-u"

def main():
    root = tk.Tk()
    root.title("m3u8Downloader -https://github.com/Leenshady/m3u8Downloader")
    
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    ww = 650
    wh = 150
    x = (sw-ww) / 2
    y = (sh-wh) / 2 - 10
    root.geometry("%dx%d+%d+%d" %(ww,wh,x,y))

    root.minsize(ww, wh)
    root.maxsize(ww, wh)

    radio = tk.IntVar()

    R1 = tk.Radiobutton(root, text="文件", variable=radio, value=1, command=selectF)  
    R1.place(x=10,y=10)

    R2 = tk.Radiobutton(root, text="链接", variable=radio, value=2, command=selectU)  
    R2.place(x=80,y=10)
    selectU()
    R2.select()

    label = tk.Label(root, text="下载链接/文件路径")
    label.place(x=10,y=50)

    entry = tk.Entry(root, bd=3, width=50)
    entry.place(x=160,y=50)

    button = tk.Button(root,text="下载", command=lambda:download(entry.get(),root))
    button.place(x=280,y=90)

    # 进入消息循环
    root.mainloop()

if __name__ == '__main__':
    main()
