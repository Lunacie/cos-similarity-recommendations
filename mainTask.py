import sys

from recommendationModule.recommendation import RecommendationModule
from dataModule.data import DataModule

from user import User
from config import Config


class MainTask :

    _recommendationModule = None

    def __init__(self, id, lng, lat, dist) :
        # 1. Data retrieval module
        dataModule = DataModule()

        # 2. Recommendations Module
        self._recommendationModule = RecommendationModule(dataModule)

        # User
        #user = User(Config['userId'], Config['lng'],
        #            Config['lat'], Config['maxDist'])
        user = User(id, lng, lat, dist)

        dataModule.setUser(user)
        dataModule.buildUserFeatures()

        self._recommendationModule.setUser(user)


    def doRecommendation(self) :

        reco = self._recommendationModule.doRecommendation()
        return(reco)
