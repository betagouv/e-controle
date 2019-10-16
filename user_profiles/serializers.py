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
    control = serializers.PrimaryKeyRelatedField(
        queryset=Control.objects.all(), write_only=True, required=False)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = (
            'id', 'first_name', 'last_name', 'email', 'profile_type',
            'organization', 'control', 'is_audited', 'is_inspector')

    def create(self, validated_data):
        profile_data = validated_data
        control = profile_data.pop('control', None)
        user_data = profile_data.pop('user')
        user_data['username'] = user_data['email']
        profile = UserProfile.objects.filter(user__username=user_data.get('email')).first()
        session_user = self.context['request'].user
        if control and control not in session_user.profile.controls.all():
            raise serializers.ValidationError(
                f"{session_user} n'est pas authorisé à modifier ce contrôle: {control}")
        action_details = {}
        action_details['sender'] = self.context['request'].user
        should_receive_email_report = False
        if profile_data.get('profile_type') == UserProfile.INSPECTOR:
            should_receive_email_report = True
        if profile:
            profile.user.first_name = user_data.get('first_name')
            profile.user.last_name = user_data.get('last_name')
            profile.organization = profile_data.get('organization')
            profile.profile_type = profile_data.get('profile_type')
            profile.send_files_report = should_receive_email_report
            profile.user.save()
            profile.save()
            if control and control not in profile.controls.all():
                # The incoming control is not already associated to this user,
                # so we know that the user is being added to this control.
                action_details['verb'] = 'added'
            else:
                action_details['verb'] = 'updated'

        else:
            user = User.objects.create(**user_data)
            profile_data['user'] = user
            profile_data['send_files_report'] = should_receive_email_report
            profile = UserProfile.objects.create(**profile_data)
            action_details['verb'] = 'added'
        action_details['action_object'] = profile
        if control:
            profile.controls.add(control)
            action_details['target'] = control
        if profile.is_inspector:
            action_details['verb'] += ' inspector user'
        if profile.is_audited:
            action_details['verb'] += ' audited user'
        action.send(**action_details)
        return profile
