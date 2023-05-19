from rest_framework import routers
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('crud', views.CRUD, basename='crud')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls'))
]
