from control.models import Question, Theme, Questionnaire, Control


def parse_word():
    control = Control.objects.create(title='mon control')
    questionnaire = Questionnaire.objects.create(title='mon questionnaire', control=control)
    theme = Theme.objects.create(title='mon theme', questionnaire=questionnaire)
    question = Question.objects.create(description='ma question', theme=theme)
    print(question)
