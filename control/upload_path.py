
def response_file_path(instance, filename):
    control_folder = instance.question.theme.questionnaire.control.reference_code or \
        f'CONTROLE-{instance.question.theme.questionnaire.control.id}'
    theme_num = instance.question.theme.numbering
    theme_folder = f'THEME-{theme_num}'
    questionaire_num = instance.question.theme.questionnaire.numbering
    questionnaire_folder = f'QUESTIONNAIRE-{questionaire_num:02}'
    question_num = instance.question.numbering
    prefixed_filename = f'Q{questionaire_num:02}-{theme_num:02}-{question_num:02}-{filename}'
    return f'{control_folder}/{questionnaire_folder}/{theme_folder}/{prefixed_filename}'
