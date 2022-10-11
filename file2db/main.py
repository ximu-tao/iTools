import tomysql
from queue import Queue

# 常用配置项
FILE_PATH = r""
TABLE_NAME = ''
COLUMN_NAMES = []

# 非常用配置项
HAS_TABLE_HEAD = True
FILE_ENCODING = 'utf-8'
READ_LINE_NUM = -1
THREAD_WORKERS_NUM = 2


def line2list(lline: str) -> list:
    lline = lline.split(",")
    lline = [x.strip() for x in lline]
    lline[3] = lline[3] + '-' + lline[4]
    del lline[4]

    return lline


tmb = tomysql.ToMySQLBuilder()
tmb.loadConfigFromTomlFile()
print(tmb.generateSQL(TABLE_NAME, COLUMN_NAMES))

weiboFile = open(FILE_PATH, encoding=FILE_ENCODING)

if HAS_TABLE_HEAD:
    weiboFile.readline()

q = Queue()
readedline = 0
while True:
    line = weiboFile.readline()
    if line == '':
        break
    line = line2list( line )
    q.put(line)
    readedline += 1
    if READ_LINE_NUM != -1 and readedline > READ_LINE_NUM:
        break

tmb.setDate(q)
tmb.startMultiple(THREAD_WORKERS_NUM)

tmb.waitAll()
