
from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework.response import Response
from api.apimodule.serializers import UserSerializer, TaskSerializer

import sys
sys.path.insert(0, './srcs')
from mainTask import MainTask

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
'''    
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
'''


class Task(object):
    def __init__(self, **kwargs):
        for field in ('id', 'score',):
            setattr(self, field, kwargs.get(field, None))

'''
reco = {
    1 : Task(id = 7224, score = 0.46565019545273256),
    2 : Task(id = 7225, score = 0.46565019545273256),
    3 : Task(id = 7226, score = 0.46565019545273256)
}
'''


class TaskViewSet(viewsets.ViewSet) :

    serializer_class = TaskSerializer
    
    def list(self, request) :
        userId = request.query_params['id']
        lng = request.query_params['lng']
        lat = request.query_params['lat']
        maxDist = request.query_params['dist']

        task = MainTask(userId, lng, lat, maxDist)
        reco = task.doRecommendation()

        res = {}
        i = 0
        for item in reco :
            res[i] = Task(id = item['id'], score = item['score'])
            i += 1

        serializer = TaskSerializer(instance = res.values(), many = True)

        #serializer = TaskSerializer(instance = reco.values(), many = True)
        return Response(serializer.data)
