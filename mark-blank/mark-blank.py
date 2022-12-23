"""
为指定的路径下的空文件与空文件夹添加标签,后序遍历法,递归实现
@title MarkBlank
@author XimuTao
"""

import os

blankTag = "#空白"

def isblank( file ):
    pass

def Mark( file , tag ):
    os.rename( file , file+tag )

def MarkBlank( path , tag):
    """
    递归
    非空白计数器:有非空白文件就加一,结束时返回
    """
    notBlankCount = 0
    fileList = os.listdir(path)
    for i in fileList:
        i = path+'\\'+i
        if os.path.isdir( i ):
            notBlankCount += MarkBlank( i , tag)
        if os.path.isfile( i ):
            if os.path.getsize( i ) == 0:
                Mark( i , tag )
            else:
                notBlankCount+=1
    if notBlankCount == 0:
        Mark( path , tag )
    return notBlankCount

MarkBlank("D:\d" , blankTag)