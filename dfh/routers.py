from django.urls import path
from rest_framework import routers
from dfh.views import *


dfh_routers = routers.DefaultRouter()
dfh_routers.register(r'get-key', GetKeyViewSet)
dfh_routers.register(r'submit', GetKeyViewSet)
