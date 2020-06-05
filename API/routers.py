from rest_framework import routers
from django.urls import path
from dfh.routers import dfh_routers


class FullRoutes(routers.DefaultRouter):
    def extend(self, router):
        self.registry.extend(router.registry)

api_router = FullRoutes()
api_router.extend(dfh_routers)


