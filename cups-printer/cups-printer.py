"""
PS: 仅适用于 Linux 环境

sudo apt install -y python-cups libcups2-dev
pip3 install pycups watchdog
"""

import os
import cups
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

WATCH_PATH = '/printer'  # 监控目录

def print_file( file ):
    print( '收到打印任务' , file )
    conn = cups.Connection()
    printers = conn.getPrinters()
    emptyDict = {}
    AvailablePrinters = list(printers.keys())
    PrinterUsing = AvailablePrinters[0]
    conn.printFile(PrinterUsing, file , "TEST", emptyDict)

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, **kwargs):
        super(FileMonitorHandler, self).__init__(**kwargs)
        self._watch_path = WATCH_PATH
        self.is_handleing = False

    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            if self.is_handleing:
                return

            self.is_handleing = True

            files = os.listdir( WATCH_PATH )

            for i in files:
                file = os.path.join( WATCH_PATH , i )
                if os.path.isdir( file ):
                    continue
                # print(file, '是一个文件')
                if i[-4:].upper() in [ ".PDF" ]:
                    # print(file, '是一个PDF文件')
                    new_path = os.path.join( WATCH_PATH , '.printed' , i )
                    os.rename( file , new_path )

                    print_file( new_path )

            print( '执行结束')
            self.is_handleing = False


if __name__ == "__main__":
    event_handler = FileMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_PATH, recursive=True)  # recursive递归的
    observer.start()
    observer.join()


