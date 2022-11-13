import pymysql
import queue
import toml
import threading
from pymysql import Connection


class ToMySQLBuilder:
    '''
    作为 Builder 和 Util 类共同使用
    '''

    # 多线程类 ToMySQL 的定义
    class ToMySQL(threading.Thread):
        '''
        对数据库的实际操作
        '''

        def __init__(self,
                     connect: Connection = None,
                     sql: str = None,
                     dataQueue: queue.Queue = None):
            super(ToMySQLBuilder.ToMySQL, self).__init__()
            self.__sql = sql
            self.__dataQueue = dataQueue
            self.__connect = connect

            self.__cursor = None

        def __init__(self):
            super(ToMySQLBuilder.ToMySQL, self).__init__()
            self.__cursor = None

        def setMysqlConnect(self, connect: Connection):
            self.__connect = connect

        def setSQL(self, sql):
            self.__sql = sql

        def submit(self, dataQueue: queue.Queue):
            self.__dataQueue = dataQueue
            return self

        def run(self) -> None:
            self.__cursor = self.__connect.cursor()
            while not self.__dataQueue.empty():
                line = self.__dataQueue.get()
                # print( self.__sql , line )
                try:
                    self.__cursor.execute(self.__sql, line)
                except Exception as e:
                    print(e)
                    print( self.__sql , line )

            self.__connect.commit()
            self.__cursor.close()
            self.__connect.close()

    # 多线程类 ToMySQL 的定义完成

    #
    def __init__(self):
        self.__data: queue.Queue = None
        self.__sql: str = None
        self.__mysqlConfig = {
            "host": '127.0.0.1',
            "port": 3306,
            "user": 'root',
            "password": '123456',
            "dbname": 'test'
        }

        self.__toMySQLList: [threading.Thread] = []

    def loadConfigFromTomlFile(self, path='config.toml'):
        config = toml.load(path)
        self.setMysqlConfig(config['mysql'])
        return self

    def setMysqlConfig(self, config: dict):
        self.__mysqlConfig.update(config)
        return self

    def generateSQL(self, tablename: str, columns: [str]) -> str:
        SQL = f"insert into {tablename}( `{'` , `'.join(columns)}`  ) VALUES( {','.join(['%s' for i in columns])}  ) "
        self.__sql = SQL
        # print(self.__sql)
        return SQL

    def setDate(self, dataQueue: queue.Queue=None):
        if dataQueue is None:
            self.__data = queue.Queue()
        self.__data = dataQueue

    def newConnect(self):
        return pymysql.connect(
            host=self.__mysqlConfig['host'],
            port=self.__mysqlConfig['port'],
            user=self.__mysqlConfig['user'],
            passwd=self.__mysqlConfig['password'],
            db=self.__mysqlConfig['dbname']
        )

    def build(self) -> ToMySQL:
        conn = self.newConnect()
        to = self.ToMySQL()
        to.setSQL(self.__sql)
        to.setMysqlConnect(conn)
        to.submit(self.__data)

        self.__toMySQLList.append(to)
        return to

    def startNew(self) -> ToMySQL:
        return self.startMultiple(1)[0]

    def startMultiple(self , workers=2) -> [ToMySQL]:
        '''
        直接以多线程方式启动多个 ToMySQL
        :return: [ToMySQL]
        '''
        assert workers  > 0 , "workers must be greater than 0"
        assert self.__data, "data is None"
        assert not self.__data.empty() , "data is empty"

        tos = []
        for i in range(workers):
            to = self.build()
            to.start()
            tos.append(to)
        return tos

    def waitAll(self):
        for thread in self.__toMySQLList:
            thread.join()


def test():
    ToMySQLBuilder().loadConfigFromTomlFile(
        "./config.toml").generateSQL('afsdf', [
        'name', 'gender', 'birthdate', 'email'])


if __name__ == '__main__':
    test()
