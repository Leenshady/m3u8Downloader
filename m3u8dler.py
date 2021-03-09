import requests
import os
import os.path
from pathlib import Path
import sys
import AESdecrypto
import traceback
import logger 
import tkinter as tk
import _thread
import tkinter.messagebox as messagebox
import GUI

headers = {'user-agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}
global num
global printer

#预处理参数
def preProcess(varType, url, p, func):
    global printer
    printer = p
    if varType=="-u":
        if url.find('?')!=-1:#判断链接是否带参数
            urlWOVar = url[0:url.rindex('?')]#去除参数
        else:
            urlWOVar = url
        if urlWOVar.startswith("http")==False or urlWOVar.endswith("m3u8")==False:#检验链接是否合法
            printer.print("The link is in the wrong format.","e")
        else:
            printer.print("Download:"+urlWOVar,"i")
            try:
                res = requests.get(url, timeout=5)#发起请求,10秒超时
            except:
                printer.print("#exception: #url:"+url+" #The request error.","e")
                printer.print(traceback.format_exc(),"e")
            else:
                if res.status_code==200:
                    if(res.text.find(".m3u8")!=-1):#主播放列表文件
                        m3u8PlaylistProcessor(url,urlWOVar,res.content,func)
                    elif(res.text.find(".ts")!=-1):#媒体播放列表
                        m3u8MediaUrlProcessor(url,urlWOVar)
                    else:
                        printer.print("fail:Link error","e")
                else:
                    printer.print("fail:Request error","e")
    elif varType=="-f":
        content = open(url,"r").read()
        if(content.find(".m3u8")!=-1):#主播放列表文件
            printer.print("The m3u8 master playlist is not supported at this time.","w")
        elif(content.find(".ts")!=-1):#媒体播放列表文件
            m3u8MediaFileProcessor(content)
        else:
            printer.print("fail:Link error","e")

# m3u8链接处理
def m3u8MediaUrlProcessor(url,urlWOVar):
    list1 = urlWOVar.split('/')
    filename = list1[-1]#获取m3u8文件名
    res = requests.get(url)#发起请求
    with open(filename,'wb') as f1:#打开文件，并写入内容
        f1.write(res.content)
    f1.close()
    m3u8MediaProcessor(url,urlWOVar,res.content.decode("utf-8"))
    return

# m3u8媒体文件处理   
def m3u8MediaProcessor(url,urlWOVar,content):#链接处理
    #print("!!!"+url)
    #print("!!!"+urlWOVar)
    #print("!!!"+content[0:200])
    list2 = content.split("\n")
    f2 = open('file.txt','wb')#file.txt用于辅助合并.ts文件
    isEncrypto = False
    if(content.find("#EXT-X-KEY")!=-1):#获取key
        for i in range(len(list2)):
            if(list2[i].find("#EXT-X-KEY")!=-1):
                key_dict = key_rvl(list2[i])
                isEncrypto=True
                break
    for i in range(len(list2)):#循环遍历
        if list2[i].find('.ts')!=-1:#获取.ts文件的下载链接
            if list2[2].find('?')!=-1:#判断是否带参数
                url2=list2[i][0:url.rindex('?')]#去除参数
            else:
                url2=list2[i]
            if list2[i].startswith('http')==False:#判断是否带协议
                printer.print(urlWOVar[0:url.rindex('/')]+'/'+list2[i],"i")
                res1 = requests.get(urlWOVar[0:url.rindex('/')]+'/'+list2[i])#不带则加上下载链接前部
            else:
                printer.print(list2[i],"i")
                res1 = requests.get(list2[i])#带协议直接下载
            tsFilePath = Path("ts/")
            if tsFilePath.exists()==False:
                os.mkdir(tsFilePath)
            f3 = open("ts\\"+str(i)+".ts",'wb')#打开.ts文件
            if isEncrypto==False:#未加密
                f3.write(res1.content)#写入.ts文件
            else:#加密
                f3.write(AESdecrypto.aesDecrypt(key_dict["KEY"],res1.content,key_dict["IV"]))#先解密，再写入.ts文件
            f3.close()
            f2.write(("file '"+os.getcwd()+"\\ts\\"+str(i)+".ts"+"'\r\n").encode())#写入file.txt
    f2.close()
    #合并TS文件
    mergeTs()

# m3u8媒体文件处理（以文件形式下载）
def m3u8MediaFileProcessor(content):
    list2 = content.split("\n")
    f2 = open('file.txt','wb')#file.txt用于辅助合并.ts文件
    isEncrypto = False
    if(content.find("#EXT-X-KEY")!=-1):#获取key
        for i in range(len(list2)):
            if(list2[i].find("#EXT-X-KEY")!=-1):
                key_dict = key_rvl(list2[i])
                isEncrypto=True
                break
    for i in range(len(list2)):#循环遍历
        if list2[i].find('.ts')!=-1:#获取.ts文件的下载链接
            if list2[2].find('?')!=-1:#判断是否带参数
                url2=list2[i][0:list2[i].rindex('?')]#去除参数
            else:
                url2=list2[i]
            if url2.startswith('http')==False:#判断是否带协议
                printer.print("File resolution error, please use the link to download.","i")
                return
            else:
                printer.print(url2,"i")
                res1 = requests.get(url2,headers=headers)
            tsFilePath = Path("ts/")
            if tsFilePath.exists()==False:
                os.mkdir(tsFilePath)
            f3 = open("ts\\"+str(i)+".ts",'wb')#打开.ts文件
            if isEncrypto==False:#未加密
                f3.write(res1.content)#写入.ts文件
            else:#加密
                f3.write(AESdecrypto.aesDecrypt(key_dict["KEY"],res1.content,key_dict["IV"]))#先解密，再写入.ts文件
            f3.close()
            f2.write(("file '"+os.getcwd()+'\\ts\\'+str(i)+".ts"+"'\r\n").encode())#写入file.txt
    f2.close()
    #合并TS文件
    mergeTs()

#播放列表处理
def m3u8PlaylistProcessor(url,urlWOVar,content,func):
    protocol = urlWOVar.split("/")[0]
    host = urlWOVar.split("/")[2]
    cttList = content.decode("utf-8").split("\n")
    info = []
    downloadUrl = []
    for i in range(len(cttList)):
        if cttList[i].startswith("#EXT-X-STREAM-INF"):
            info.append(cttList[i])
        if cttList[i].endswith(".m3u8"):
            downloadUrl.append(cttList[i])
    printer.print("###m3u8PlaylistProcessor info:"+str(info),"i")
    printer.print("###m3u8PlaylistProcessor downloadUrl:"+str(downloadUrl),"i")
    
    func(info,protocol,host,url,downloadUrl)

#命令行获取用户输入
def cliInputAndDownload(info,protocol,host,url,downloadUrl):
    printer.print("Please select the video you want to download.","i")
    for i in range(len(info)):
        printer.print(str(i)+" "+info[i],"i")
    num = int(input("input:"))
    m3u8Playlist_download(protocol,host,url,downloadUrl,num)

#下载m3u8 master文件里的m3u8媒体文件
def m3u8Playlist_download(protocol,host,url,downloadUrl,num):
    printer.print('### m3u8Playlist_download: num='+str(num),"i")
    mediaUrl = downloadUrl[num]
    if mediaUrl.find('?')!=-1:#判断链接是否带参数
        mediaUrlWOVar = url[0:url.rindex('?')]#去除参数
    else:
        mediaUrlWOVar = mediaUrl
    if(mediaUrl.startswith("http")):
        printer.print("m3u8Media:"+mediaUrl,"i")
        m3u8MediaUrlProcessor(mediaUrl,mediaUrlWOVar)
    else:
        urlType1 = url[0:url.rindex("/")+1]+mediaUrl
        code = -1
        try:
            code = requests.get(urlType1,timeout=5).status_code#测试链接，解决不同的链接组合方式
        except Exception as e:
            #printer.print(str(e.args),"e")
            #printer.print("=====","e")
            #printer.print(traceback.format_exc(),"e")
            pass
        finally:
            if(code==200):
                printer.print("m3u8Media:"+url[0:url.rindex("/")+1]+mediaUrl+"\r\n"+url[0:url.rindex("/")+1]+mediaUrlWOVar,"i")
                m3u8MediaUrlProcessor(url[0:url.rindex("/")+1]+mediaUrl,url[0:url.rindex("/")+1]+mediaUrlWOVar)
            else:
                printer.print("m3u8Media:"+protocol+"//"+host+"/"+mediaUrl+"\r\n"+protocol+"//"+host+"/"+mediaUrlWOVar,"i")
                m3u8MediaUrlProcessor(protocol+"//"+host+"/"+mediaUrl,protocol+"//"+host+"/"+mediaUrlWOVar)

#key处理
def key_rvl(keyStr):
    list1 = keyStr.split(",")
    key_dict = {"METHOD":"","KEY":"","IV":""}
    for i in range(len(list1)):
        if(list1[i].find("METHOD")!=-1):
            key_dict["METHOD"] = list1[i][list1[i].index("METHOD")+7:len(list1[i])]
            continue
        if(list1[i].find("URI")!=-1):
            uri = list1[i][list1[i].index("URI")+5:len(list1[i])-1]
            printer.print(uri,"i")
            key_dict["KEY"] = requests.get(uri).content
            continue
        if(list1[i].find("IV")!=-1):
            key_dict["IV"] = list1[i][list1[i].index("IV")+3:len(list1[i])]
            continue
    if len(key_dict["IV"])==0:
        key_dict["IV"]=key_dict["KEY"]
    printer.print(str(key_dict),"i")
    return key_dict

#调用ffmpeg合并ts文件
def mergeTs():
    main = "ffmpeg.exe -f concat -safe 0 -i file.txt -c copy out.mp4 -y"#ffmpeg合并命令
    r_v = os.system(main)#调用ffmpeg合并.ts文件
    printer.print('###ffmpeg result'+str(r_v),"i")
    printer.print('###done!',"i")
    return r_v

#启动线程下载，避免阻塞GUI
def thread_download(protocol,host,url,downloadUrl,num):
    try:
        _thread.start_new_thread( m3u8Playlist_download, (protocol,host,url,downloadUrl,num) )
        messagebox.showinfo('提示','已经开始下载！')
    except:
        printer.print("###Thread Error","e")



    
    
