
from dataModule.activities import ActivityList
from dataModule.features import FeatureList

from dataModule.database.db_mysql import Dbmysql
from dataModule.database.db_postgres import Dbpostgres


from user import User

class DataModule :

    _activities = None
    _currentUser = None

    def __init__(self) :
        pass
        

    def setUser(self, user) :
        self._currentUser = user
        coords = self._currentUser.getCoords()
        
        # getting activities for this user
        self._activities = ActivityList(coords[0], coords[1],
                                        user.getMaxDistance())
    

    def buildUserFeatures(self) :
        self._currentUser.setFeatures(FeatureList(self._currentUser))
        

    def getActivities(self) :
        return self._activities
