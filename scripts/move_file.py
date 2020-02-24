import os

def move_file(response_file_id, new_order):
  response_file = ResponseFile.objects.get(id=response_file_id)
  initial_path = response_file.file.path
  initial_name = response_file.file.name
  initial_prefix = f'Q{response_file.question.theme.questionnaire.numbering:02}-T{response_file.question.theme.numbering:02}-{response_file.question.numbering:02}'
  new_prefix = f'Q{response_file.question.theme.questionnaire.numbering:02}-T{response_file.question.theme.numbering:02}-{(new_order + 1):02}'

  new_name = initial_name.replace(initial_prefix, new_prefix, 1)
  new_path = settings.MEDIA_ROOT + '/' + new_name

  response_file.file.name = new_name
  os.rename(initial_path, new_path) # needs sudo rights

  response_file.save()
