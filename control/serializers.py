from django.contrib.auth import get_user_model

from rest_framework import serializers

from utils.serializers import DateTimeFieldWihTZ

from .models import Question, Questionnaire, ResponseFile, Theme, Control


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ResponseFileSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    creation_date = DateTimeFieldWihTZ(source='created', format='%A %d %B %Y')
    creation_time = DateTimeFieldWihTZ(source='created', format='%X')

    class Meta:
        model = ResponseFile
        fields = ('id', 'url', 'basename', 'creation_date', 'creation_time', 'author')


class QuestionSerializer(serializers.ModelSerializer):
    response_files = ResponseFileSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'description', 'response_files', 'theme')


class ThemeSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Theme
        fields = ('id', 'title', 'questionnaire', 'questions')
        # not serialized : order


class QuestionnaireSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True, read_only=True)
    control = serializers.PrimaryKeyRelatedField(queryset=Control.objects.all(), required=True)

    class Meta:
        model = Questionnaire
        fields = ('id', 'title', 'sent_date', 'end_date', 'description', 'control', 'themes')
        # not serialized (yet) : file, order
