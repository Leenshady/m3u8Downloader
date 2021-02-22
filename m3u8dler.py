import requests
import os
import sys
import AESdecrypto


'''if len(sys.argv)<=1:#判断有没有链接
    print("Please add a download link after the script.")
else:
    url = sys.argv[1]
    if url.find('?')!=-1:#判断链接是否带参数
        urlWOVar = url[0:url.rindex('?')]#去除参数
    else:
        urlWOVar = url
    if urlWOVar.startswith("http")==False or urlWOVar.endswith("m3u8")==False:#检验链接是否合法
        print("The link is in the wrong format.")
    else:
        print("Download:"+urlWOVar)'''
def m3u8MediaDownload(url,urlWOVar):
    list1 = urlWOVar.split('/')
    filename = list1[-1]#获取m3u8文件名
    res = requests.get(url)#发起请求
    with open(filename,'wb') as f1:#打开文件，并写入内容
        f1.write(res.content)
    f1.close()
    list2 = str(res.content).split('\\n')
    f2 = open('file.txt','wb')#file.txt用于辅助合并.ts文件
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
            with open(str(i)+".ts",'wb') as f3:#打开.ts文件
                #print(res1.content[0:200])
                if str(res.content).find("#EXT-X-KEY")==-1:
                    f3.write(res1.content)#写入.ts文件
                else:
                    for j in range(len(list2)):
                        if list2[j].find("#EXTINF")==1:
                            break
                        if list2[j].find("#EXT-X-KEY")!=-1:
                            s = list2[j]
                            method = s[s.index("METHOD")+7:s.index(",")]
                            uri = s[s.index("URI")+5:len(s)-1]
                            print(uri)
                            key = requests.get(uri).content
                            print(key)
                            f3.write(AESdecrypto.aesDecrypt(key,res1.content))#写入.ts文件
            f3.close()
            f2.write(("file '"+os.getcwd()+'\\'+str(i)+".ts"+"'\r\n").encode())#写入file.txt
    f2.close()
    main = "ffmpeg.exe -f concat -safe 0 -i file.txt -c copy out.mp4"#ffmpeg合并命令
    r_v = os.system(main)#调用ffmpeg合并.ts文件
    print(r_v)
    print('done!')
    return

def m3u8PlaylistProcesser(url,urlWOVar,content):
    protocol = urlWOVar.split("/")[0]
    host = urlWOVar.split("/")[2]
    cttList = content.split("\\n")
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
        m3u8MediaDownload(mediaUrl,mediaUrlWOVar)
    else:
        print(protocol+"//"+host+"/"+mediaUrl,protocol+"//"+host+"/"+mediaUrlWOVar)
        m3u8MediaDownload(protocol+"//"+host+"/"+mediaUrl,protocol+"//"+host+"/"+mediaUrlWOVar)
    return



    
