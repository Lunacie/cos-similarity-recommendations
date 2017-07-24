
import math

from dataModule.database.db_reco import DbReco
from dataModule.database.dbConfig import recoDb

from list import DbList

from dataModule.features import FeatureList

class ActivityList(DbList) :

    _categories = None
    _maxDist = 0

    def __init__(self, lng, lat, maxDist) :
        super().__init__()

        self._maxDist = float(maxDist)

        request = "SELECT id, productName, advertisedPrice, "
        request += "hasSortPriority, "
        request += """(((acos(sin(("""+ lat + """ * pi()/180))
                 * sin((`p`.`latitude`*pi()/180)) + cos(("""+ lat + """*pi()/180))
                 * cos((`p`.`latitude` * pi()/180))
                 * cos((("""+ lng + """ - `p`.`longitude`)
                 * pi()/180)))) * 180/pi()) * 60 * 1.1515 * 1.609344) AS distance
                 FROM `product` `p` """
        request += " WHERE productStatus='Active'"
        request += " HAVING distance <= "+ str(maxDist)
        request += " LIMIT 500"

        self._db = DbData()
        self._res = self._db.execute(request)
        self.mapActivities()

        #self._categories = CategoryList()
        #self._categories.matchToActivities(self)

        self.getFeaturesVector()


    def getFeaturesVector(self) :
        db = DbReco()
        for element in self._list :
            request = "SELECT vector from "
            request += recoDb['db']['schema'] + ".itemVectors "
            request += "WHERE productId='"+ str(element['id']) +"'"
            self._res = db.execute(request)

            #element["features"] = FeatureList.unserialize(self._res[0][0])
            element["features"] = self._res[0][0]


    # mapping the data into activities dictionaries
    def mapActivities(self) :
        for element in self._res :
                self._list.append({
                           "id": element[0],
                           "name": element[1],
                           "budget": element[2],
                           "curated" : element[3],
                           "distance" : self.normalizeDistance(element[4]),
                           '''
                           "categories" : [],
                           "genres" : [],
                           '''
                           "features" : None})




    def normalizeDistance(self, str) :
        value = float(str)
        value = value / self._maxDist
        return value

    # OVERLOADS
    # this method is gonna return the element matching
    # the id by splitting them in half and calling itself recursively
    # until the element is found

    def getItemById(self, id, min = 0, max = 0) :

        if (self._list == None) :
                return None

        # first recursion level
        if (max == 0) :
                #init max
                max = len(self._list) - 1
                #check if too big
                if (self._list[max]['id'] < id) :
                    return None
                #check if too small
                elif (self._list[0]['id'] > id) :
                    return None

        #print ("\nmin, max", min, max)
        # real median
        rmedian = min + ((max - min) / 2)
        #print("real median : ",rmedian)

        #in case it's the first element
        median = self._list[int(rmedian)]['id']
        if (id == median):
            return self._list[int(rmedian)]


        if (max - min == 1) :
            rmedian = max
        rmedian = int(rmedian)


        median = self._list[rmedian]['id']
        #print("id : ", median)

        #print("comparing id to median : ", id, median)
        # found it
        if (id == median):
                return self._list[rmedian]

        # Could not find
        if (rmedian <= 0 or max - min <= 1) :
            #print("Count not find id ", id)
            return None


        # id is smaller
        elif (id < median):
                #print("smaller")
                return self.getItemById(id, min, rmedian)
        # id is bigger
        elif (id > median):
                #print("bigger")
                return self.getItemById(id, rmedian, max)
