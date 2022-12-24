"""
为指定的路径下的空文件与空文件夹添加标签,后序遍历法,递归实现
@title MarkBlank
@author XimuTao
"""

import os

blankTag = "空白"

blankList = []
rootPath = './'

__isRename__ = True
__isSave__ = True
__tag__ = ''

def saveFile( path ):
    if __isSave__ == True:
        with open( rootPath + '\\blank.txt' , encoding='UTF-8' , mode = 'a+') as f:
            # for i in blankList:
            #     f.write( i )
            #     f.write( '\n' )

            f.write( path )
            f.write( '\n' )

def reName( file ):
    global __tag__
    p , n =  os.path.split( file )
    ind = n.find( __tag__ )

    if n.find( '$' ) == -1:
        tag__ = '$'+__tag__
    else:
        tag__ = __tag__
    # print(file)
    # print( ind )
    if ind == -1:
        # os.rename( file , file+__tag__ )
        n , s = os.path.splitext(file)
        # print( n )
        # print( s )
        os.rename( file , n+tag__+s )

def Mark( file ):
    """
    为 file 添加 tag ,
    """
    blankList.append( file )
    saveFile(file)
    if __isRename__ == True:
        reName( file )

def isBlank( path ):
    """
    递归
    非空白计数器,有非空白文件就加一,结束时返回
    """
    notBlankCount = 0
    fileList = os.listdir(path)
    for name in fileList:
        i = path+'\\'+name
        if os.path.isdir( i ):
            notBlankCount += isBlank( i )
        if os.path.isfile( i ):
            if os.path.getsize( i ) == 0:
                Mark( i )
            else:
                notBlankCount+=1
    if notBlankCount == 0:
        Mark( path )
    return notBlankCount

def MarkBlank( path , isRename = True , isSave = True , tag = ''):
    global rootPath , __isRename__ , __isSave__ , __tag__
    if tag == '':
        __tag__ = '#'+blankTag
    else:
        __tag__ = '#'+tag
    __isRename__ = isRename
    __isSave__ = isSave
    rootPath = path
    isBlank( path )
    # saveFile( path )

if __name__ == '__main__':
    # tag = blankTag
    # MarkBlank( "D:\d" , tag = '')
    p = input( )

    MarkBlank( p , tag = '')