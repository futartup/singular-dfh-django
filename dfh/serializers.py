from rest_framework.serializers import ModelSerializer
from dfh.models import *


class KeySerializer(ModelSerializer):
    class Meta:
        model = Key
        fields = '__all__'
        