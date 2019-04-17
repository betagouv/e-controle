from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import UserProfile


User = get_user_model()


class ControlPKField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        user = self.context['request'].user
        queryset = user.profile.controls.all()
        return queryset


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.pk', read_only=True)
    controls = ControlPKField(many=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'first_name', 'last_name', 'email', 'profile_type',
            'organization', 'controls', 'is_active')
        extra_kwargs = {'controls': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data
        controls_data = profile_data.pop('controls')
        user_data = profile_data.pop('user')
        user_data['username'] = user_data['email']
        profile = UserProfile.objects.filter(user__email=user_data.get('email')).first()
        if not profile:
            user = User.objects.create(**user_data)
            profile_data['user'] = user
            profile_data['send_files_report'] = True
            profile = UserProfile.objects.create(**profile_data)
        for control_data in controls_data:
            profile.controls.add(control_data)
        return profile
