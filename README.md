# 中文

## m3u8 下载器

一个 m3u8 下载器  
使用 Python 编写，支持 AES-128 解密，支持图形界面

### 环境  
Python3.8  

### 依赖库  
+ requests  
+ pycryptodome  
  
怎么安装依赖库
```
pip3 install requests
pip3 install pycryptodome
```

### 怎么使用

注意：m3u8 下载器需要搭配 ffmpeg 使用，把 ffmpeg.exe 放在和 run.py 的同级目录下  
ffmpeg 下载链接：https://ffmpeg.org/download.html

#### 命令行
打开CMD，进入m3u8Donwloader所在目录  
+ 使用链接下载  
```
run.py -u https://example.com/index.m3u8
```

+ 使用本地文件下载  
```
run.py -f example.m3u8
```
  
#### 界面  
打开CMD，进入m3u8Donwloader所在目录  
```
GUI.py
```  
![image](https://user-images.githubusercontent.com/27936579/110605603-3eac8980-81c4-11eb-8f54-e3f8607ef4e5.png)

---
  
# English

## m3u8Downloader

An m3u8 Downloader.  
Written in Python, Support AES-128 decryption, support graphical interface.


### Environment  
Python3.8  

### Dependency Library  
+ requests  
+ pycryptodome  
  
How to install dependency library  
```
pip3 install requests
pip3 install pycryptodome
```

### How to use it

Note:The m3u8Downloader require ffmpeg,please put the ffmpeg.exe into the same directory as run.py.  
ffmpeg download link: https://ffmpeg.org/download.html  

#### Command Line  
+ Use the url to download  
```
run.py -u https://example.com/index.m3u8
```

+ Use local files to download  
```
run.py -f example.m3u8
```

#### GUI  
Open the CMD and enter the directory of m3u8dongwloader.  
```
GUI.py
```  
![image](https://user-images.githubusercontent.com/27936579/110605603-3eac8980-81c4-11eb-8f54-e3f8607ef4e5.png)
