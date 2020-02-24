import os

response_file_id = 670
# move from question 3 to 2
initial_question = 'Q01-T01-03'
new_question = 'Q01-T01-02'

response_file = ResponseFile.objects.get(id=response_file_id)
initial_path = response_file.file.path
initial_name = response_file.file.name

new_name = initial_name.replace(initial_question, new_question, 1)
new_path = settings.MEDIA_ROOT + '/' + new_name

response_file.file.name = new_name
os.rename(initial_path, new_path) # needs sudo rights

response_file.save()
