from rest_framework import serializers
from Machinery import models
from Machinery.help import helpers

class UserSerializer(serializers.ModelSerializer):
    class meta:
        model = models.Users
        fields = ('fname', 'lname', 'password', 'email', 'msisdn')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):

        user = models.Users(
            fname=validated_data['fname'],
            lname=validated_data['lname'],
            email=validated_data['email'],
            msisdn=validated_data['msisdn']      
        )

        user.set_password(validated_data['password'])
        user.save()
        helpers.create_stripe_user(validated_data['email'])

        return user
    
