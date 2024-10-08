from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    """
    User ViewSet
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    