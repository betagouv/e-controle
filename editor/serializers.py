from rest_framework import serializers

from control.models import Questionnaire

class UpdateEditorQuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ('editor',)
        extra_kwargs = {
            'editor': {
                'required': True,
                'allow_null': True,
            }
        }
