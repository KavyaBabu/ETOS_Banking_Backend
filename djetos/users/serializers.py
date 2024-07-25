from django.contrib import admin
from rest_framework import serializers

from .models import User

admin.autodiscover()


# first we define the serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")
