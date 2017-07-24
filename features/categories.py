

from list import DbList
from genre import GenreList


class CategoryList(DbList):

    _res = []
    _list = []

    _genres = None

    def __init__(self) :
        super().__init__()

        rows = "id, productId, productCategoryId"
        request = "SELECT "+ rows +" FROM productHasCategory"

        self._db = DbData()
        self._res = self._db.execute(request)

        if (self._res):
                self.mapCategories()

        self._genres = GenreList()


    # mapping the data into activities dictionaries
    def mapCategories(self) :
        for element in self._res :
                self._list.append({
                           "id" : element[0],
                           "productId" : element[1],
                           "productCategoryId" : element[2]})



    def matchToActivities(self, activities) :
        for element in self._list :
            if  activities.getItemById(element["productId"]):
                activities.getItemById(element["productId"])["categories"].append(element["productCategoryId"])
                self._genres.matchToCategories(activities.getItemById(element["productId"]))
