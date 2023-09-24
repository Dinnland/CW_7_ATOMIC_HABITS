from rest_framework import serializers

from users.models import User


# Это сериализатор \/
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        print('create')
        print(validated_data)
        user = User.objects.create_user(**validated_data)
