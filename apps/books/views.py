from .models import Library, Book
from .serializers import (LibrarySerializer, BookSerializer, SearchUserByIdSerializer,
                          BookTransactionSerializer, SearchBookByIdSerializer)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import MultipleObjectsReturned
from rest_framework.exceptions import ValidationError


class LibraryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows library to be viewed or edited.
    """
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    
    @action(detail=True, methods=['post'])
    def add_book(self, request, *args, **kwargs):
        """Registra libro a la biblioteca"""
        instance = self.get_object()
        serializer = SearchBookByIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.add_book(serializer.validated_data['book'])
        return Response({'msg': self.get_serializer(instance).data, 'result': True}, 201)
    
    @action(detail=True, methods=['post'])
    def borrow_book(self, request, *args, **kwargs):
        """Toma un libro prestado"""
        instance = self.get_object()
        serializer = BookTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            if not instance.lend_book(**serializer.validated_data):
                return Response({'msg': 'El libro no esta disponible', 'result': False}, 400)
        except (Book.DoesNotExist, MultipleObjectsReturned):
            raise ValidationError("titulo no encontrado")
        return Response({'msg': 'Libro prestado', 'result': True}, 201)

    @action(detail=True, methods=['post'])
    def get_back_book(self, request, *args, **kwargs):
        """Devuelve el libro"""
        instance = self.get_object()
        serializer = BookTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            if instance.get_back_book(**serializer.validated_data):
                return Response({'msg': 'Libro devuelto', 'result': True}, 201)
            else:
                return Response({'msg': 'El libro no esta rentado por el usuario', 'result': False}, 400)
        except (Book.DoesNotExist, MultipleObjectsReturned):
            raise ValidationError("titulo no encontrado")
    
    @action(detail=True, methods=['post'])
    def register_user(self, request, *args, **kwargs):
        """registra usuario"""
        instance = self.get_object()
        serializer = SearchUserByIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.register_user(serializer.validated_data['user'])
        return Response({'msg': 'Usuario registrado', 'result': True}, 201)
        

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows book to be viewed or edited.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
