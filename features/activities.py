
import math
import time
import datetime

from dataModule.database.db_reco import DbReco
from list import DbList
from dataModule.database.dbConfig import recoDb


from categories import CategoryList
from dataModule.features import FeatureList
from desirability import DesirabilityList

class ActivityList(DbList) :

    _db = None
    _dbReco = None
    _categories = None

    _list = []

    def __init__(self) :
        super().__init__()

        rows = "id, productName, advertisedPrice, hasSortPriority,"
        rows += "publicId"
        request = "SELECT "+ rows +" FROM product WHERE country='Australia'"
        request += "ORDER BY id"

        self._db = dbData()
        self._res = self._db.execute(request)
        self.mapActivities()

        # TODO : update this to not build full category/genre
        # each call
        self._categories = CategoryList()
        self._categories.matchToActivities(self)

        self.buildAvailabilities()
        self._desirability = DesirabilityList(self._list)

        self.getFeaturesList()


    def buildAvailabilities(self) :

        # checking if activity has availabilities
        max = 0
        now = int(time.time())
        print ("Retrieving timestamp for activities("
               +str(len(self._list))+")",
               end='', flush=True)
        for item in self._list :
            #print (".", end='', flush=True)
            request = '''
            SELECT p.id,
            IF(`p`.`bookingMode` = 'INVENTORY',
                (SELECT UNIX_TIMESTAMP(`startTime`)
                FROM `productAvailability` WHERE `productId` = `p`.id
                AND `startTime` > DATE_ADD(CURRENT_TIMESTAMP,
                INTERVAL IFNULL(`p`.minimumNoticeMinutes,0) MINUTE)
                AND `seatsAvailable` > 0
                ORDER BY `startTime` ASC LIMIT 1), null)
            as 'nextAvailabilityTimeStamp'
            FROM `product` `p` WHERE p.id='''
            request += str(item['id'])
            request += " ORDER BY `nextAvailabilityTimeStamp` ASC"
            self._res = self._db.execute(request)
            if (self._res[0][1] is not None) :
                item['available'] = self._res[0][1]
                if (self._res[0][1] > max) :
                    max = self._res[0][1]
            else :
                item['available'] = 0
        print("\n")

        value = (now - max) / (now - max)
        print("now : ", value)

        value = (max - max) / (now - max)
        print("biggest : ", value)

        for item in self._list :
            if (item['available'] != 0) :
                value = (item['available'] - max) / (now - max)
                #uncomment this if you want to test timestamp normals
                #print(datetime.datetime.utcfromtimestamp(item['available']))
                #print("normalized : ", value, "\n")
                item['available'] = value



    def getFeaturesList(self) :
        self._dbReco = DbReco()
        self._dbReco.truncateRestart(
            recoDb['db']['schema'] + ".itemVectors")

        # TODO : matching the features to the activites
        #        takes too long
        #        build an extension module instead
        values = []
        for element in self._list :
            features = FeatureList(None, element)
            #element["features"] = features
            element["itemVector"] = features.serialize()
            current = {
                "productId" : str(element["id"]),
                "vector" : str(element["itemVector"])
            }
            values.append(current)
            print(current)

        request = "INSERT INTO "+ recoDb['db']['schema']
        request += ".itemVectors(productId, vector) "
        request += "VALUES(%(productId)s, %(vector)s)"
        self._res = self._dbReco.executeMany(request, values)
        self._res = self._dbReco.commit()

    # mapping the data into activities dictionaries
    def mapActivities(self) :
        for element in self._res :
                data = {
                           "id": element[0],
                           "name": element[1],
                           "budget": self.normalizeBudget(element[2]),
                           "curated" : element[3],
                           "publicId" : element[4],
                           "categories" : [],
                           "distance" : "x",
                           "genres" : [],
                           "features" : None}
                self._list.append(data)

    def normalizeBudget(self, nb) :
        if (nb is None):
            return 0

        if (nb < 200) :
            return 1
        elif (nb < 500 ) :
            return 2
        else :
            return 3


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
