import tkinter as tk
import os
import m3u8dler
import logger

option = ""

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
    button = tk.Button(root1,text="下载", command=lambda:m3u8dler.thread_download(protocol,host,url,downloadUrl,radio.get()))
    button.pack(side=tk.TOP, expand=tk.YES, fill=tk.Y)
    root1.mainloop()
    return

def download(url):
    m3u8dler.preProcess(option,url,logger.LogPrinter(),masterPlaylistOptGUI)

def selectF():
    global option
    option="-f"

def selectU():
    global option
    option="-u"

def main():
    root = tk.Tk()
    radio = tk.IntVar()

    R1 = tk.Radiobutton(root, text="文件", variable=radio, value=1, command=selectF)  
    R1.pack(side=tk.TOP, expand=tk.YES)

    R2 = tk.Radiobutton(root, text="链接", variable=radio, value=2, command=selectU)  
    R2.pack(side=tk.TOP, expand=tk.YES)
    selectU()
    R2.select()

    label = tk.Label(root, text="下载链接/文件路径")
    label.pack(side = tk.TOP,expand=tk.YES)

    entry = tk.Entry(root, bd=3, width=50)
    entry.pack(side =tk.TOP, expand=tk.YES)

    button = tk.Button(root,text="下载", command=lambda:download(entry.get()))
    button.pack(side=tk.TOP, expand=tk.YES, fill=tk.Y)

    # 进入消息循环
    root.mainloop()

if __name__ == '__main__':
    main()
