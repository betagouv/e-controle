def questionnaire_file_path(instance, filename):
    questionnaire = instance
    control_folder = questionnaire.control.reference_code
    questionaire_num = questionnaire.numbering
    questionnaire_folder = f'Q{questionaire_num:02}'
    path = f'{control_folder}/{questionnaire_folder}/{filename}'
    return path


class PathBuilder(object):

    def __init__(self, file_object, filename):
        self.file_object = file_object
        self.filename = filename
        self.control_folder = file_object.question.theme.questionnaire.control.reference_code or \
            f'CONTROLE-{file_object.question.theme.questionnaire.control.id}'
        self.questionaire_num = file_object.question.theme.questionnaire.numbering
        self.questionnaire_folder = f'Q{self.questionaire_num:02}'
        self.theme_num = file_object.question.theme.numbering
        self.theme_folder = f'T{self.theme_num:02}'
        self.question_num = file_object.question.numbering
        self.questionnaire_path = f'{self.control_folder}/{self.questionnaire_folder}'
        self.theme_path = f'{self.questionnaire_path}/{self.theme_folder}'

    def get_question_file_path(self):
        question_path = f'{self.questionnaire_path}/ANNEXES-AUX-QUESTIONS'
        path = f'{question_path}/{self.filename}'
        return path

    def get_response_file_path(self):
        prefix = f'Q{self.questionaire_num:02}-T{self.theme_num:02}-{self.question_num:02}'
        response_filename = f'{prefix}-{self.filename}'
        path = f'{self.theme_path}/{response_filename}'
        return path


def question_file_path(instance, filename):
    path = PathBuilder(file_object=instance, filename=filename)
    return path.get_question_file_path()


def response_file_path(instance, filename):
    path = PathBuilder(file_object=instance, filename=filename)
    return path.get_response_file_path()
