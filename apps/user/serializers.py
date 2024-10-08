from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    book_set = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'
   