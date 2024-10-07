from rest_framework import routers
from django.urls import include, path
from .views import LibraryViewSet, BookViewSet


router = routers.DefaultRouter()
router.register(r'library', LibraryViewSet)
router.register(r'book', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]