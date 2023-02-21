from rest_framework import serializers

from accounts.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(write_only=True, required=False, allow_blank=True, default='')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'name',)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'avatar', 'rows_to_recalculate_available',)
