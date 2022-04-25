from rest_framework import serializers

from authentication.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "position", "date_of_birth", "username", "password")
