"""
调用7z命令批量压缩文件
@title 批量压缩
@author XimuTao
@version 1.0
"""
import os

_dir__ = r''
_7Z_PATH__ = r'C:\Program Files\7-Zip\7z.exe'

if len(_dir__)==0:
    _dir__ = input()

dirlist = os.listdir(_dir__)

from concurrent.futures import ThreadPoolExecutor

import subprocess

# p=subprocess.Popen( "tree > tree.txt" )
# return_code=p.wait()
# os.popen("tree > tree.txt")

executor = ThreadPoolExecutor(max_workers=5)


def compression(_path_):
    aimsName = _path_ + ".zip"
    cmd = _7Z_PATH__+' a "%s" "%s"' % (aimsName, _path_)
    # print( cmd )
    p = subprocess.Popen(cmd, shell=False)
    return_code = p.wait()
    return return_code

print(dirlist)
for name in dirlist:
    # name = os.path.abspath(name)
    name = os.path.join(_dir__, name)
    # print( name )
    if os.path.isdir(name):
        executor.submit(compression, (name))
