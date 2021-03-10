import tkinter as tk
import os
import m3u8dler
import logger
import time

option = ""

def progressBarGUI():
    pgb = tk.Tk()
    pgb.title("下载")
    v = tk.StringVar(master=pgb)
    tk.Label(pgb, text='下载进度:', ).place(x=20, y=30)
    progress = tk.Label(pgb, textvariable=v)
    v.set('0%')
    progress.place(x=110, y=30)
    v.set('1%')
    pgb.update()
    while(int(m3u8dler.progressValue)!=1):
        v.set(str(m3u8dler.progressValue*100)[0:5]+"%")
        pgb.update()
        time.sleep(0.02)
    v.set('下载完成！')
    pgb.mainloop()

def masterPlaylistOptGUI(info,protocol,host,url,downloadUrl):
    root1 = tk.Tk()
    #这里是个巨坑，master参数一定要填上，不然radio不会绑定到Radiobutton上
    radio = tk.IntVar(master=root1)
    r = []
    for i in range(len(info)):
        m3u8dler.printer.print("###GUI.py p i="+str(i),"i")
        r.append(tk.Radiobutton(root1, text=info[i], variable=radio, value=i))
        r[i].pack(side=tk.TOP, expand=tk.YES, fill=tk.Y)
        r[i].select()
    button = tk.Button(root1,text="下载", command=lambda:m3u8dler.thread_download(protocol,host,url,downloadUrl,radio.get(),root1))
    button.pack(side=tk.TOP, expand=tk.YES, fill=tk.Y)
    root1.mainloop()
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
    root.minsize(650, 150)
    root.maxsize(650, 150)  
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
