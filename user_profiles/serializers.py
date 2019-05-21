from django.contrib.auth import get_user_model

from actstream import action
from rest_framework import serializers

from control.models import Control

from .models import UserProfile


User = get_user_model()


class RemoveControlSerializer(serializers.Serializer):
    control = serializers.PrimaryKeyRelatedField(queryset=Control.objects.all())


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.pk', read_only=True)
    controls = serializers.PrimaryKeyRelatedField(many=True, queryset=Control.objects.all())
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = (
            'id', 'first_name', 'last_name', 'email', 'profile_type',
            'organization', 'controls', 'is_audited', 'is_inspector')
        extra_kwargs = {'controls': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data
        controls_data = profile_data.pop('controls')
        user_data = profile_data.pop('user')
        user_data['username'] = user_data['email']
        profile = UserProfile.objects.filter(user__username=user_data.get('email')).first()
        action_details = {}
        action_details['sender'] = self.context['request'].user
        if profile:
            profile.user.first_name = user_data.get('first_name')
            profile.user.last_name = user_data.get('last_name')
            profile.organization = profile_data.get('organization')
            profile.profile_type = profile_data.get('profile_type')
            profile.user.save()
            profile.save()
            action_details['verb'] = 'update user'
        else:
            user = User.objects.create(**user_data)
            profile_data['user'] = user
            profile_data['send_files_report'] = True
            profile = UserProfile.objects.create(**profile_data)
            action_details['verb'] = 'add user'
        action_details['action_object'] = profile
        controls_to_be_added = [c for c in controls_data if c not in profile.controls.all()]
        for control in controls_to_be_added:
            session_user = self.context['request'].user
            if control not in session_user.profile.controls.all():
                raise serializers.ValidationError(
                    f"{session_user} n'est pas authorisé à modifier ce contrôle: {control}")
            profile.controls.add(control)
            action_details['verb'] = 'add user'
            action_details['target'] = control
        action.send(**action_details)
        return profile
