from rest_framework import serializers
from .models import Library, Book
from apps.user.models import User


class LibrarySerializer(serializers.ModelSerializer):
    book_set = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Library
        fields = '__all__'
        extra_kwargs = {
            'user_register': {'required': False}
        }

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'user_borrow',)
        extra_kwargs = {
            'user_borrow': {'required': True, 'allow_null': False}
        }

class SearchBookByIdSerializer(serializers.Serializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

class SearchUserByIdSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())