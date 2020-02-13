from django.contrib.auth import get_user_model

from rest_framework import serializers

from utils.serializers import DateTimeFieldWihTZ

from .models import Control, Question, QuestionFile, Questionnaire, ResponseFile, Theme


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'id')


class ResponseFileSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    creation_date = DateTimeFieldWihTZ(source='created', format='%a %d %B %Y')
    creation_time = DateTimeFieldWihTZ(source='created', format='%X')

    class Meta:
        model = ResponseFile
        fields = ('id', 'url', 'basename', 'created', 'creation_date', 'creation_time', 'author', 'is_deleted', 'question')


class ResponseFileTrashSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseFile
        fields = ('id', 'is_deleted')


class QuestionFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionFile
        fields = ('id', 'url', 'basename', 'file', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    response_files = ResponseFileSerializer(many=True, read_only=True)
    question_files = QuestionFileSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'description', 'order', 'question_files', 'response_files', 'theme')


class ThemeSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    order = serializers.IntegerField(required=False)

    class Meta:
        model = Theme
        fields = ('id', 'title', 'order', 'questionnaire', 'questions')


# Serializers for displaying control_detail.html
class ControlDetailUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'id',)


class QuestionnaireSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True, read_only=True)
    editor = ControlDetailUserSerializer(read_only=True, required=False)
    modified_date = DateTimeFieldWihTZ(source='modified', format='%a %d %B %Y', read_only=True)
    modified_time = DateTimeFieldWihTZ(source='modified', format='%X', read_only=True)

    class Meta:
        model = Questionnaire
        fields = ('id', 'title', 'sent_date', 'end_date', 'description', 'control', 'themes', 'is_draft', 'editor',
                  'title_display', 'numbering', 'modified_date', 'modified_time')

        extra_kwargs = {'control': {'required': True}}
        # not serialized (yet) : file, order


class ControlSerializer(serializers.ModelSerializer):
    questionnaires = QuestionnaireSerializer(many=True, read_only=True)

    class Meta:
        model = Control
        fields = ('id', 'title', 'depositing_organization', 'reference_code', 'questionnaires')


class ControlUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control
        fields = ('id', 'title', 'depositing_organization')


class QuestionUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    order = serializers.IntegerField(required=False)

    class Meta:
        model = Question
        fields = ('id', 'order', 'description')


class ThemeUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    questions = QuestionUpdateSerializer(many=True, required=False)

    class Meta:
        model = Theme
        fields = ('id', 'title', 'questions')


class QuestionnaireUpdateSerializer(serializers.ModelSerializer):
    themes = ThemeUpdateSerializer(many=True, required=False)

    class Meta:
        model = Questionnaire
        fields = ('id', 'title', 'sent_date', 'end_date', 'description', 'control', 'themes', 'is_draft')
        extra_kwargs = {
            'control': {
                'required': True,
                'allow_null': False,
            }
        }


class ControlDetailQuestionnaireSerializer(serializers.ModelSerializer):
    editor = ControlDetailUserSerializer(read_only=True, required=False)
    modified_date = DateTimeFieldWihTZ(source='modified', format='%a %d %B %Y', read_only=True)
    modified_time = DateTimeFieldWihTZ(source='modified', format='%X', read_only=True)

    class Meta:
        model = Questionnaire
        fields = ('id', 'title', 'numbering', 'url', 'is_draft', 'sent_date', 'end_date', 'editor',
            'modified_date', 'modified_time')


class ControlDetailControlSerializer(serializers.ModelSerializer):
    questionnaires = ControlDetailQuestionnaireSerializer(many=True, read_only=True)

    class Meta:
        model = Control
        fields = ('id', 'title', 'depositing_organization', 'reference_code', 'questionnaires')
