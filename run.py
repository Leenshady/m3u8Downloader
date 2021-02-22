import requests
import sys
import m3u8dler

if len(sys.argv)<=1:#判断有没有链接
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
        print("Download:"+urlWOVar)
    res = requests.get(url)#发起请求
    if(str(res.content).find(".m3u8")!=-1):#主播放列表文件
        m3u8dler.m3u8PlaylistProcesser(url,urlWOVar,str(res.content))
    elif(str(res.content).find(".ts")!=-1):#媒体播放列表
        m3u8dler.m3u8MediaDownload(url,urlWOVar)
    else:
        print("fail.")
