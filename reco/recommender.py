
import math
from operator import attrgetter

from recommendationModule.recommender import Recommender
from dataModule.features import FeatureList

class Recommender(Recommender) :

    _result = []


    def __init__ (self, dataModule) :
        Recommender.__init__(self, dataModule)


    def doRecommendation(self) :

        activities = self._dataModule.getActivities()

        userVector = self._user.getFeatures().getVector()

        #+ aditional feature
        #userVector.append(1)

        for activity in  activities:
            itemVector = FeatureList.unserialize(activity['features'],
                                                 activity['distance'])

            # + aditionnal feature
            #itemVector.append(1)

            res = self.cosine_similarity(userVector, itemVector)

            self._result.append({
                    "score" : res,
                    "name" : activity['name'],
                    "id" : activity['id'],
                    "curated" : activity['curated'],
                    #"itemVector" : itemVector
                    })

        self._sorted = sorted(self._result, key=lambda k: k['score'] ,reverse=True)

        self._result = []
        #print(userVector)
        last = 0
        for item in self._sorted :
            if ((last != 0) and (item['score'] == last)) :
                pass
            else :
                self._result.append(item)
            last = item['score']

        return self._result


    # (v1 dot v2) / {||v1||*||v2||)
    def cosine_similarity(self, v1, v2) :
        sumXX = 0
        sumXY = 0
        sumYY = 0

        max = len(v1)
        for i in range(max) :
            x = v1[i]
            y = v2[i]

            sumXX += x * x
            sumYY += y * y
            sumXY += x * y

        value = math.sqrt(sumXX * sumYY)
        if (value == 0) :
            return 0
        return sumXY / value
