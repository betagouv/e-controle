
def response_file_path(instance, filename):
    control_folder = instance.question.theme.questionnaire.control.reference_code or \
        f'CONTROLE-{instance.question.theme.questionnaire.control.id}'
    questionnaire_folder = instance.question.theme.questionnaire.reference_code or \
        f'QUESTIONNAIRE-{instance.question.theme.questionnaire.id}'
    theme_folder = instance.question.theme.reference_code or \
        f'THEME-{instance.question.theme.id}'
    prefixed_filename = f'{instance.question_numbering}-{filename}'
    return f'{control_folder}/{questionnaire_folder}/{theme_folder}/{prefixed_filename}'
