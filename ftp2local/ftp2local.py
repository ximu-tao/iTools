import ftplib

import os

from ftplib import FTP

def ftp_isdir( filename ):
    # 💩 判断FTP文件是否为目录
    return filename.find(".") == -1


def uniformity_check( ftp, ftpfile, localfile ):
    # 💩 判断文件是否已被下载过
    return os.path.exists( localfile )


# 连接ftp服务器
def ftpConnect(ftpserver, port, usrname, password):
    ftp = FTP()
    try:
        ftp.connect(ftpserver, port)
        ftp.login(usrname, password)
    except Exception as e:
        print( e )
    else:
        print(ftp.getwelcome())  # 打印登陆成功后的欢迎信息
        return ftp


# 下载单个文件
def ftpDownloadFile(ftp, ftpfile, localfile):
    # print( localfile , os.path.exists( localfile ) )
    if uniformity_check(ftp, ftpfile, localfile ):
        print( localfile , "已存在，不再下载" )
        return

    print( 'download: ' , ftpfile )
    # fid = open(localfile, 'wb') # 以写模式打开本地文件
    bufsize = 1024
    with open(localfile, 'wb') as fid:
        ftp.retrbinary('RETR {0}'.format(ftpfile), fid.write, bufsize)  # 接收服务器文件并写入本地文件
    return True


# 下载整个目录下的文件
def ftpDownload(ftp, ftpath, localpath):
    print('Remote Path: {0}'.format(ftpath))
    if not os.path.exists(localpath):
        os.makedirs(localpath)
    ftp.cwd(ftpath)

    filelist = ftp.nlst()
    filelist.remove('.')
    filelist.remove('..')

    for file in filelist:

        local = os.path.join(localpath, file)

        if ftp_isdir(file):  # 判断是否为子目录
            if not os.path.exists(local):
                os.makedirs(local)
            ftpDownload(ftp, file, local)  # 递归调用
        else:
            ftpDownloadFile(ftp, file, local)
    ftp.cwd('..')
    return True


# 退出ftp连接
def ftpDisConnect(ftp):
    ftp.quit()


# 程序入口
if __name__ == '__main__':
    # 输入参数
    ftpserver = ''
    port = 21
    usrname = ''
    pwd = ''
    ftpath = ''
    localpath = ''

    ftp = ftpConnect(ftpserver, port, usrname, pwd)
    flag = ftpDownload(ftp, ftpath, localpath)
    print(flag)
    ftpDisConnect(ftp)
    print("\n+-------- OK!!! --------+\n")
