
from dataModule.features import FeatureList

class User :

    _id = 0
    _lng = ""
    _lat = ""
    _maxDist = ""
    
    _features = None

    def __init__(self, id, lng, lat, maxDist) :
        self._id = id
        self._lng = lng
        self._lat = lat
        self._maxDist = maxDist
        

    def getCoords(self) :
        return (self._lng, self._lat)
        
    def getMaxDistance(self) :
        return (self._maxDist)
        
    def setFeatures(self, preferences) :
        self._features = preferences

    def getFeatures(self) :
        return self._features

    def getId(self) :
        return self._id
