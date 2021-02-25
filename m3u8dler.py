import requests
import os
import os.path
from pathlib import Path
import sys
import AESdecrypto
import traceback

headers = {'user-agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}
def m3u8MediaUrlProcessor(url,urlWOVar):
    list1 = urlWOVar.split('/')
    filename = list1[-1]#获取m3u8文件名
    res = requests.get(url)#发起请求
    with open(filename,'wb') as f1:#打开文件，并写入内容
        f1.write(res.content)
    f1.close()
    m3u8MediaProcessor(url,urlWOVar,res.content.decode("utf-8"))
    return
    
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
                print(urlWOVar[0:url.rindex('/')]+'/'+list2[i])
                res1 = requests.get(urlWOVar[0:url.rindex('/')]+'/'+list2[i])#不带则加上下载链接前部
            else:
                print(list2[i])
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
    main = "ffmpeg.exe -f concat -safe 0 -i file.txt -c copy out.mp4"#ffmpeg合并命令
    r_v = os.system(main)#调用ffmpeg合并.ts文件
    print(r_v)
    print('done!')
    return

def m3u8MediaFileProcessor(content):#文件处理
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
                print("File resolution error, please use the link to download.")
                return
            else:
                print(list2[i])
                res1 = requests.get(list2[i],headers=headers)
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
    main = "ffmpeg.exe -f concat -safe 0 -i file.txt -c copy out.mp4"#ffmpeg合并命令
    r_v = os.system(main)#调用ffmpeg合并.ts文件
    print(r_v)
    print('done!')
    return

def m3u8PlaylistProcessor(url,urlWOVar,content):
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
    print(info)
    print(downloadUrl)
    print("Please select the video you want to download.")
    for i in range(len(info)):
        print(str(i)+" "+info[i])
    num = int(input("input:"))
    mediaUrl = downloadUrl[num]
    if mediaUrl.find('?')!=-1:#判断链接是否带参数
        mediaUrlWOVar = url[0:url.rindex('?')]#去除参数
    else:
        mediaUrlWOVar = mediaUrl
    if(mediaUrl.startswith("http")):
        print("m3u8Media:"+mediaUrl)
        m3u8MediaUrlProcessor(mediaUrl,mediaUrlWOVar)
    else:
        urlType1 = url[0:url.rindex("/")+1]+mediaUrl
        code = -1
        try:
            code = requests.get(urlType1,timeout=5).status_code#测试链接，解决不同的链接组合方式
        except Exception as e:
            #print("#exception: #url:"+urlType1+" #The request error.")
            pass
        finally:
            if(code==200):
                print("m3u8Media:"+url[0:url.rindex("/")+1]+mediaUrl,url[0:url.rindex("/")+1]+mediaUrlWOVar)
                m3u8MediaUrlProcessor(url[0:url.rindex("/")+1]+mediaUrl,url[0:url.rindex("/")+1]+mediaUrlWOVar)
            else:
                print("m3u8Media:"+protocol+"//"+host+"/"+mediaUrl,protocol+"//"+host+"/"+mediaUrlWOVar)
                m3u8MediaUrlProcessor(protocol+"//"+host+"/"+mediaUrl,protocol+"//"+host+"/"+mediaUrlWOVar)
        
    return

def key_rvl(keyStr):#key处理
    list1 = keyStr.split(",")
    key_dict = {"METHOD":"","KEY":"","IV":""}
    for i in range(len(list1)):
        if(list1[i].find("METHOD")!=-1):
            key_dict["METHOD"] = list1[i][list1[i].index("METHOD")+7:len(list1[i])]
            continue
        if(list1[i].find("URI")!=-1):
            uri = list1[i][list1[i].index("URI")+5:len(list1[i])-1]
            print(uri)
            key_dict["KEY"] = requests.get(uri).content
            continue
        if(list1[i].find("IV")!=-1):
            key_dict["IV"] = list1[i][list1[i].index("IV")+3:len(list1[i])]
            continue
    if len(key_dict["IV"])==0:
        key_dict["IV"]=key_dict["KEY"]
    print(key_dict)
    return key_dict


    
