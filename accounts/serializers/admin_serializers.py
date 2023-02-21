from rest_framework import serializers

from accounts.models import User


class UserAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data.get('password')
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
            instance.save()

    class Meta:
        model = User
        fields = '__all__'
