from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import ResponseFile, Question, Comment


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ResponseFileSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = ResponseFile
        fields = ('id', 'url', 'basename', 'creation_date', 'author')

class QuestionSerializer(serializers.ModelSerializer):
    response_files = ResponseFileSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'response_files')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True) 

    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author', many = False, write_only = True) 
    question = serializers.PrimaryKeyRelatedField(queryset = Question.objects.all(), allow_null = True, many = False, required = False)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'author_id', 'text', 'creation_date', 'question')
