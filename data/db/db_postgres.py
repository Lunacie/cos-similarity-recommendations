import psycopg2

from dataModule.database.db import Db

class   Dbpostgres(Db) :


        def __init__(self) :
           Db.__init__(self)
        
        def connect(self, dbConfig, bindPort = 5432) :
           # Now for the postgres connect
           print("DbpostGres() : ")
           print("user : " + dbConfig['user'])
           print("host : " + dbConfig['host'] + " " +
                 str(dbConfig['port']))
           print("db : " + dbConfig['database'])

           params = {
                   'database' : dbConfig['database'], 
                   'user' : dbConfig['user'], 
                   'host' : dbConfig['host'], 
                   'password' : dbConfig['passwd'], 
                   'port' : dbConfig['port']}
                
           self._db = psycopg2.connect(**params)
           self._cursor = self._db.cursor()

           
        def execute(self, request):
            self._cursor.execute(request)
            self._data = self._cursor.fetchall()
            return self.getResult()
                
        def commit(self):
            self._db.commit( )

        def close(self) :
            self._db.close()
            self._db = None
            self._cursor = None
            self._data = None
