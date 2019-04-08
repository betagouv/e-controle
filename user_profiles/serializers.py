from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import UserProfile


User = get_user_model()


class ControlPKField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        user = self.context['request'].user
        queryset = user.profile.controls.all()
        return queryset


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    controls = ControlPKField(many=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'profile_type', 'organization', 'controls')
        extra_kwargs = {'controls': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data
        controls_data = profile_data.pop('controls')
        user_data = profile_data.pop('user')
        user_data['username'] = user_data['email']
        user = User.objects.create(**user_data)
        profile_data['user'] = user
        profile_data['send_files_report'] = True
        profile = UserProfile.objects.create(**profile_data)
        for control_data in controls_data:
            profile.controls.add(control_data)
        return profile
