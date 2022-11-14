from webdav4.client import Client
import os

__client__: Client = None

def download_files(from_path: str, to_path, chunk_size: int = None, callback=None):
    """
    下载 Webdav 文件, 下载后会删除云端文件
    :param from_path:
    :param to_path:
    :param chunk_size:
    :param callback:
    :return:
    """

    if __client__.isfile(from_path):
        __client__.download_file(from_path, to_path, chunk_size, callback)
        __client__.remove(from_path)
        print( '已下载', from_path)
    else:
        file_list = __client__.ls(path=from_path, detail=False)

        try:
            os.mkdir(to_path)
        except FileExistsError:
            pass
        for i in file_list:
            download_files(i, os.path.join(to_path, os.path.basename(i)), chunk_size, callback)

def download_dir( base_url , auth ,  from_path: str, to_path ):
    global __client__
    __client__ = Client(base_url=base_url,
                    auth=auth )
    download_files( from_path , to_path )

if __name__ == '__main__':
    WEBDAV_PATH = ''
    LOCAL_PATH = r""
    download_dir(base_url='',
                    auth=('', '') ,
                 from_path=WEBDAV_PATH , to_path=LOCAL_PATH)

# download_files(WEBDAV_PATH, PATH)