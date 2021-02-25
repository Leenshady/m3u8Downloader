import requests
import sys
import traceback
import m3u8dler

if len(sys.argv)<=2:#判断有没有链接或路劲
    print("Please add a download link or path after the script.")
else:
    varType = sys.argv[1]
    if varType=="-u":
        url = sys.argv[2]
        if url.find('?')!=-1:#判断链接是否带参数
            urlWOVar = url[0:url.rindex('?')]#去除参数
        else:
            urlWOVar = url
        if urlWOVar.startswith("http")==False or urlWOVar.endswith("m3u8")==False:#检验链接是否合法
            print("The link is in the wrong format.")
        else:
            print("Download:"+urlWOVar)
        try:
            res = requests.get(url, timeout=5)#发起请求,10秒超时
        except Exception as e:
            print("#exception: #url:"+url+" #The request error.")
            print(traceback.format_exc())
        else:
            if res.status_code==200:
                if(res.text.find(".m3u8")!=-1):#主播放列表文件
                    m3u8dler.m3u8PlaylistProcessor(url,urlWOVar,res.content)
                elif(res.text.find(".ts")!=-1):#媒体播放列表
                    m3u8dler.m3u8MediaUrlProcessor(url,urlWOVar)
                else:
                    print("fail:Link error")
            else:
                print("fail:Request error")
    elif varType=="-f":
        path = sys.argv[2]
        content = open(path,"r").read()
        if(content.find(".m3u8")!=-1):#主播放列表文件
            print("The m3u8 master playlist is not supported at this time.")
        elif(content.find(".ts")!=-1):#媒体播放列表文件
            m3u8dler.m3u8MediaFileProcessor(content)
        else:
            print("fail:Link error")
