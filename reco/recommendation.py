
from recommendationModule..recommender import Recommender

from dataModule.data import DataModule

class RecommendationModule :

    _dataModule = None
    _user = None

    Recommender = None


    def __init__(self, dataModule) :
        self._dataModule = dataModule

        self.Recommender = Recommender(dataModule)


    def setUser(self, user) :
        self._user = user

        self.Recommender.setUser(user)


    def doRecommendation(self) :

        recommender = self.Recommender
        #recommender = self.dynamicRecommender

        reco = recommender.doRecommendation()
        #reco = self.sortCurated(reco)

        i = 0
        for item in reco :
            print(i, ". ", item)
            i += 1
        return reco
