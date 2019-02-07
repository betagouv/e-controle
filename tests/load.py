import random

from control import models as control_models

from tests import factories


N_CONTROLS = 1
N_USER_PER_CONTROL = 6
N_QUESTIONNAIRE_PER_CONTROL = 5
N_THEME_PER_QUESTIONNAIRE = 5
N_QUESTION_PER_THEME = 10
N_RESPONSE_FILE_PER_QUESTION = 10
N_QUESTION_FILE_PER_QUESTION = 1


def populate_db(number_of_controls=N_CONTROLS):
    for _ in range(number_of_controls):
        control = factories.ControlFactory()
        print(f'Populate control {control}')
        user_list = []
        for _ in range(N_USER_PER_CONTROL):
            user = factories.UserFactory()
            user.profile.control = control
            user.profile.save()
            user_list.append(user)
        print(f'Populate users: {user_list}')
        for _ in range(N_QUESTIONNAIRE_PER_CONTROL):
            questionnaire = factories.QuestionnaireFactory(control=control)
            print(f'\tPopulate questionnaire: {questionnaire}')
            for _ in range(N_THEME_PER_QUESTIONNAIRE):
                theme = factories.ThemeFactory(questionnaire=questionnaire)
                print(f'\tPopulate theme: {theme}')
                for _ in range(N_QUESTION_PER_THEME):
                    question = factories.QuestionFactory(theme=theme)
                    print(f'\tPopulate question: {question}')
                    for _ in range(N_RESPONSE_FILE_PER_QUESTION):
                        user = random.choice(user_list)
                        factories.ResponseFileFactory(question=question)
                    for _ in range(N_QUESTION_FILE_PER_QUESTION):
                        factories.QuestionFileFactory(question=question)
                    count_r_files = control_models.ResponseFile.objects.count()
                    count_q_files = control_models.QuestionFile.objects.count()
                    print(f'\tNumber of response files so far: {count_r_files}')
                    print(f'\tNumber of question files so far: {count_q_files}')
