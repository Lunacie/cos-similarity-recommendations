from dataModule.database.db_postgres import Dbpostgres
from dataModule.database.dbConfig import recoDb

class DbReco:
        
        class __singleton(Dbpostgres):

          def __init__(self): 
                Dbpostgres.__init__(self)

                '''
                if (recoDb['ssh']['host'] == "localhost") :
                  self.connect(recoDb['db'])
                  return
                print(recoDb)
                # if host is remote
                tunnel = SSHTunnelForwarder(
                        (recoDb['ssh']['host'], 22),
                        ssh_username = recoDb['ssh']['user'],
                        ssh_password = recoDb['ssh']['passwd'],
                        ssh_private_key = recoDb['ssh']['key'],
                        remote_bind_address=('127.0.0.1',
                                recoDb['db']['port']))
                
                if (tunnel is None) :
                        return None
                tunnel.start()
                print("ssh tunnel created (reco)")
               
                # db
                bindPort = tunnel.local_bind_port
                self._tunnel = tunnel
                '''
                self.connect(recoDb['db'])
                
          def execute(self, request):
                self._cursor.execute(request)
                self._data = self._cursor.fetchall()
                return self.getResult()
                        
          def executeMany(self, request, values):
              self._cursor.executemany(request, values)

          def truncateRestart(self, table):
              request = "TRUNCATE "+ table +" RESTART IDENTITY"
              print(request)
              self._cursor.execute(request)
              self.commit()

          '''
          def closeTunnel(self) :
                print("Closing tunnel (reco)")
                self._tunnel.close()
          '''
                                
        def __new__(cls) :
            if (DbReco.instance is None) :
                DbReco.instance = DbReco.__singleton()
            return DbReco.instance
            
        instance = None
