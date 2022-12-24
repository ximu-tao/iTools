"""
随机重命名指定文件夹的文件
@title 随机重命名
@author XimuTao
@version 1.0
"""
import re
from xeger import Xeger
import os

RENAME_FILE_SUFFIX = { ".jpg" ,".png"}
# 需要重命名的文件类型(后缀名)

IS_RENAEM_DIR = False
# 是否重命名文件夹

RENAME_TEMPLATE = r'[A-Z]{16}'
# 随机命名模板

RENAMER_PATH = r""
# 目标路径

_RENAME_FILE_SUFFIX_ = set()
for i in RENAME_FILE_SUFFIX:
    _RENAME_FILE_SUFFIX_.add( i.upper() )

_x = Xeger()

try:
    asaiugfieugsdifgsidfug = _x.xeger( RENAME_TEMPLATE )
except re.error:
    print("模板有问题")
    exit(1)

if not os.path.exists(RENAMER_PATH):
    print( "文件夹不存在" )
    exit(2)


def generate():
    return _x.xeger( RENAME_TEMPLATE )

def rename( path , isdir=False):
    suffix = ""

    dirname = os.path.dirname(path)

    if not isdir:
        suffix = os.path.splitext(path)[-1]

    new_file_name = generate()+suffix

    os.rename( path , os.path.join( dirname , new_file_name ) )


def recursion( path ):
    if not os.path.isabs( path ):
        path = os.path.abspath( path )

    if os.path.isfile( path ):
        suffix = os.path.splitext(path)[-1].upper()
        if suffix in _RENAME_FILE_SUFFIX_:
            rename( path )
        return

    _file_list_ = os.listdir( path )

    for i in _file_list_:
        recursion( os.path.join( path , i ) )

    if IS_RENAEM_DIR:
        rename( path , isdir=True )

if __name__ == '__main__':
    recursion( RENAMER_PATH )