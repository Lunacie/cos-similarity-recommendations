

from list import List

from dataModule.db_mysql import Dbmysql

class GenreList(List):

    _res = []
    _list = []
    
    def __init__(self) :
        super().__init__()

        rows = "id, productCategoryId, genreId"
        request = "SELECT "+ rows +" FROM productCategoryHasGenre"

        self.db = Dbmysql()
        self._res = self.db.execute(request)
        
        if (self._res):
                self.mapGenres()

    
    # mapping the data into activities dictionaries
    def mapGenres(self) :
        for element in self._res :
                self._list.append({
                           "id" : element[0],
                           "productCategoryId" : element[1], 
                           "genreId" : element[2]})
                
           

    def matchToCategories(self, activity) :
        
        for category in activity['categories'] :
            for genre in self._list :
                if genre['productCategoryId'] == category :
                    activity['genres'].append(genre['genreId'])
