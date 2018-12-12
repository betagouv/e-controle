
def response_file_path(instance, filename):
    question_folder = instance.question.id
    prefixed_filename = f'1.1-{filename}'
    return f'{question_folder}/{prefixed_filename}'
