
class   Db :

        _user = ""
        _password = ""
        _host = ""
        _database = ""

        _db = None
        _cursor = None
        _data = None

        
        def connect(self) :
                pass
        
        def execute(self, request):
                pass
                
        # this overloads the [] operator
        def __getitem__(self, key) :
            if (key >= len(self._data)) :
                return None
            return self._data[key]

        def __len__(self) :
            if (self._data is None) :
                return 0
            return len(self._data)

        def getResult(self) :
                if (self._data is None) :
                    return None
                res = []
                for element in self._data :
                        res.append(element)
                return res
    
        def close(self) :
                pass
