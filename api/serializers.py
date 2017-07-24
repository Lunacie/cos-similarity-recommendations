
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

        
'''
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
'''     


class TaskSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    score = serializers.FloatField()

    def create(self, validatedData):
        return Task(id = None, **validatedData)

    def update(self, instance, validatedData):
        for field, value in validatedData.items():
            setattr(instance, field, value)
            return instance
