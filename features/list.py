
from dataModule.database.db import Db

class DbList :

    _dbmysql = None
    _dbpsql = None
    
    _list = []
    _res = []



    def __init__(self) :
        pass
        
    
    '''
    def execRequestCommit(self, request) :
        self.prepareRequest()
        self.execRequestPending(request)
        self.commitDb()

        
    def execRequestPending(self, request) :
        self._db.execute(request)
        self._res = self._db.getResult()

    def commitDb(self) :
        self._db.commit()
        self._db.close()
    ''' 
    
     # OVERLOADS
            
    def __getitem__(self, key) :
         if (self._list is None or key >= len(self._list)) :
             return None
         return self._list[key]

    def __len__(self) :
        if (self._list is None) :
            return 0
        return len(self._list)

    def __str__(self) :
        return str(self._list)


    def __iter__(self) :
        for x in self._list :
            yield x
