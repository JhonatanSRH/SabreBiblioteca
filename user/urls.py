from rest_framework import routers
from django.urls import include, path
from .views import UserViewSet


router = routers.DefaultRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]