from .models import Library, Book
from .serializers import LibrarySerializer, BookSerializer
from rest_framework import permissions, viewsets


class LibraryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows library to be viewed or edited.
    """
    queryset = Library.objects.all().order_by('-date_joined')
    serializer_class = LibrarySerializer
    #permission_classes = [permissions.IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows book to be viewed or edited.
    """
    queryset = Book.objects.all().order_by('-date_joined')
    serializer_class = BookSerializer
    #permission_classes = [permissions.IsAuthenticated]
