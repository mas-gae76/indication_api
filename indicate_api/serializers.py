from rest_framework import serializers
from .models import History, Counter, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CounterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Counter
        extra_kwargs = {
                            'type': {'read_only': True}
                       }
        fields = ('name', 'user', 'value')


class HistorySerializer(serializers.ModelSerializer):
    counter = CounterSerializer(many=True)

    class Meta:
        model = History
        extra_kwargs = {
                            'date': {'read_only': True},
                            'type': {'read_only': True}
                       }
        fields = ('id', 'date', 'type', 'value', 'consumption', 'counter')