import pymysql
from dataModule.database.db import Db

class   Dbmysql(Db) :

        def __init__(self) :
                Db.__init__(self)

        def connect(self) :
            '''
            self._db = pymysql.connect(
                    port = str(bindPort),
                    user = self._user,
                    passwd = self._password,
                    db = self._database);
            '''

            self._db = pymysql.connect(
                    port = self._port,
                    user = self._user,
                    passwd = self._password,
                    db = self._database,
                    host = self._host   );
            self._cursor = self._db.cursor()


        def execute(self, request):
                self._cursor.execute(request)
                self._data = self._cursor.fetchall()
                return self.getResult()

        def getResult(self) :
                if (self._data is None) :
                        return None
                res = []
                for element in self._data :
                        res.append(element)
                return res


        def close(self) :
                self._db.close()
                self._db = None
                self._cursor = None
                self._data = None



        def commit(self):
                self._db.commit()
