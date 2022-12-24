# 需要安装模块
# pip install requests "requests[socks] toml bs4"
import os
from bs4 import BeautifulSoup as bs
import requests
import toml
from urllib.parse import urlparse

config = toml.load( open('./config.toml' , mode='r' , encoding='utf-8') )
httpProxy = "%s:%s"%( config['proxy']['host'] , config['proxy']['port'] )

proxies = {
    'http': 'http://' + httpProxy,
    'https': 'http://' + httpProxy,
}

# 文件名不能包含的字符
notFileName = ['/', '\\', ':', '*', '?', '"', '<', '>', '|' , '.']

baseDLPath = './'
if 'dlpath' in config['download']:
    baseDLPath = os.path.join(config['download']['dlpath'])

if not os.path.exists( baseDLPath ):
    os.makedirs( baseDLPath )

urls = open('./urls.txt' , mode='r' , encoding='utf-8')
# print( urls )
# print( urls.readline() )
exception = []
for url in urls.readlines():
    url = url.split('|')[0].strip()
    # print( url )
    response = requests.get(url, proxies=proxies)
    # print(response.text)

    html=bs(response.text,'html.parser')
    dirName = html.title.text[0:90]
    for char in dirName:
        if char in notFileName:
            dirName = dirName.replace(char, '')
    newPath = os.path.join( baseDLPath , dirName )

    if not os.path.exists( newPath ):
        os.mkdir( newPath )
    else:
        print( newPath , "已存在" )

    imgs = html.select('img')
    count = len(imgs)
    print( html.title.text , "[000/%03d]"%count , end="" )
    pageinfoPath = os.path.join(newPath, "pageinfo.txt" )
    if not os.path.exists( pageinfoPath ):
        with open(os.path.join(newPath, "pageinfo.txt" ), "w") as f:
            f.write(url)

            f.write( os.linesep )
            f.write( str(count) )
            f.write( os.linesep )
            f.write( os.linesep )
            for i in imgs:
                f.write(i.attrs['src'])
                f.write(os.linesep)

    if count==0:
        exception.append( url )
        print()
        continue

    for imgNum in range(0,count):
        res = urlparse(url)
        # print("域名", res.scheme + '://' + res.netloc)
        imgUrl = res.scheme + '://' + res.netloc+ imgs[imgNum].attrs['src']
        if imgs[imgNum].attrs['src'].startswith('https://'):
            imgUrl = imgs[imgNum].attrs['src']

        if imgs[imgNum].attrs['src'].startswith('http://'):
            imgUrl = imgs[imgNum].attrs['src']

        # print( imgUrl )
        imgFilePath = os.path.join( newPath , "%03d%s"%( imgNum , imgUrl[-4:] ))
        if os.path.exists( imgFilePath ):
            continue
        response = requests.get(imgUrl, proxies=proxies)
        # print(newPath)
        of = open( imgFilePath , "wb")
        of.write(response.content)
        print("\b"*10 , "[%03d/%03d]"%( imgNum+1 , count) , end='' )

    print()

urls.close()

urls = open('./urls.txt' , mode='a' , encoding='utf-8')
if config.get('completion')['clearUrls']:
    urls.write("下载完成, 异常数量%d"%len(exception))

print("异常数量" , len(exception) , exception )