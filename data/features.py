

from list import DbList


weights = {
    "distance" : 2,
    "category" : 1,
    "genre" : 0.5,
    "budget" : 1,
    "curated" : 2.5,
    "available" : 1,
    "desirability" : 1
}

class FeatureList(DbList) :

    _user = None
    _activity = {}

    _list = []

    _features = {}

    _isUser = False


    def __init__(self, user = None, activity = {}) :

        self._user = user
        self._activity = activity

        self.db = dbData()

        # building feature list for user
        if user is not None :
            self._isUser = True
            # (user) Building genres
            rows = "genreId"
            request = "SELECT "+ rows +" FROM userPrefersGenre "
            request += "WHERE userId='" + user.getId() + "'"
            self._res = self.db.execute(request)
            genres = self.mapFeatures(self._res)

            # (user) Bulding categories
            rows = "productCategoryId"
            request = "SELECT "+ rows +" FROM userPrefersCategory "
            request += "WHERE userId='" + user.getId() + "'"
            self._res = self.db.execute(request)
            categories = self.mapFeatures(self._res)

            # (user) Bulding budget feature
            rows = "preferenceGroupBudget"
            request = "SELECT "+ rows +" FROM user "
            request += "WHERE id='" + user.getId() + "'"
            self._res = self.db.execute(request)
            budget = self.mapFeatures(self._res)


            self.buildFeaturesList(self.weight(1, "distance"),
                                   categories,
                                   genres,
                                   self.weight(budget[0], "budget"),
                                   self.weight(1, "curated"),
                                   self.weight(1, "available"),
                                   self.weight(1, "desirability"))

        # bulding feature list for activity
        else :
            self.buildFeaturesList(activity['distance'],
                                   activity['categories'],
                                   activity['genres'],
                                   activity['budget'],
                                   activity['curated'],
                                   activity['available'],
                                   activity['desirability'])


    def weight(self, value, index) :
        if value is None :
            return 0
        return value * weights[index]

    def mapFeatures(self, list) :
        ret = []
        for element in list :
            ret.append(element[0])
        return ret

    # mapping the data into Preferences dictionaries
    def buildFeaturesList(self, distance, categories, genres, budget, curated, available, desirability) :

        # TODO: not every call
        self.buildFullList()

        # distance
        self._features["distance"][0] = distance

        # budget
        self._features["budget"][0] = budget

        # curated
        self._features["curated"][0] = curated

        # available
        self._features["available"][0] = available

        # desirability
        self._features["desirability"][0] = desirability


        # genres
        max = len(self._features["genres"])
        if (max > 0) :
            for index in genres:
                i = 0
                for i in range (max) :
                    if (self._features["genres"][i]["id"] == index) :
                        if (self._isUser == True) :
                            self._features["genres"][i]["value"] = 1 * weights['genre']
                        else :
                            self._features["genres"][i]["value"] = 1


        # categories
        max = len(self._features["categories"])
        if (max > 0) :
            for index in categories:
                i = 0
                for i in range (max) :
                    if (self._features["categories"][i]["id"] == index) :
                        if (self._isUser == True) :
                            self._features["categories"][i]["value"] = 1 * weights['category']
                        else :
                            self._features["categories"][i]["value"] = 1



    def buildFullList(self) :

        self._list = []

        request = "SELECT id FROM productCategory ORDER BY id"
        self._res = self.db.execute(request)
        categories = self._res

        request = "SELECT id FROM genre ORDER by id"
        self._res = self.db.execute(request)
        genres = self._res

        self._features['distance'] = []
        self._features['distance'].append(0)

        self._features['budget'] = []
        self._features['budget'].append(0)

        self._features['curated'] = []
        self._features['curated'].append(0)

        self._features['available'] = []
        self._features['available'].append(0)

        self._features['desirability'] = []
        self._features['desirability'].append(0)

        i = 0
        self._features['genres'] = []
        for current in genres :
            self._features['genres'].append({"id" : current[0],
                                             "value" : 0})

        i = 0
        self._features['categories'] = []
        for current in categories :
            self._features['categories'].append({"id" : current[0],
                                                 "value" : 0})


    def getVector(self) :
        ret = []

        #distance
        ret.append(self._features['distance'][0])
        #budget
        ret.append(self._features['budget'][0])
        #curated
        ret.append(self._features['curated'][0])
        #available
        ret.append(self._features['available'][0])
        #desirability
        ret.append(self._features['desirability'][0])
        #genres
        for element in self._features['genres'] :
            ret.append(element['value'])
        #categories
        for element in self._features['categories'] :
            ret.append(element['value'])
        return ret



    def serialize(self) :
        ret = ""

        #distance
        ret += str(self._features['distance'][0]) + ' '
        #budget
        ret += str(self._features['budget'][0]) + ' '
        #curated
        ret += str(self._features['curated'][0]) + ' '
        #available
        ret += str(self._features['available'][0]) + ' '
        #desirability
        ret += str(self._features['desirability'][0]) + ' '
        #genres
        for element in self._features['genres'] :
            ret += str(element['value']) + ' '
        #categories
        for element in self._features['categories'] :
            ret += str(element['value']) + ' '

        return ret

    def unserialize(str, distance) :
        tmp = str.split(' ')
        max = len(tmp)
        ret = []
        i = 0

        # distance
        ret.append(distance * weights['distance'])
        i += 1

        # budget
        value = float(tmp[i])
        ret.append(value * weights['budget'])
        i += 1

        # curated
        value = float(tmp[i])
        ret.append(value * weights['curated'])
        i += 1

        # available
        value = float(tmp[i])
        ret.append(value * weights['available'])
        i += 1

        # desirability
        value = float(tmp[i])
        ret.append(value * weights['desirability'])
        i += 1

        count = i
        # genres
        while (i < 15 + count) :
            item = tmp[i]
            if (len(item) > 0) :
                value = float(item[0])
                if (value != 0 ) :
                    ret.append(value * weights['genre'])
                else :
                    ret.append(0)

            i += 1

        # categories
        while (i < max) :
            item = tmp[i]
            if (len(item) > 0) :
                value = float(item[0])
                if (value != 0 ) :
                    ret.append(value * weights['category'])
                else :
                    ret.append(0)
            i += 1

        return ret

    def getItemById(self, id) :
        pass
