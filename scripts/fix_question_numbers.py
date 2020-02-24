# 1. Lister les questions mal numerotées
count = 0
print('question.id', ',', 'theme.id', ',', 'questionnaire.id', ',', 'index', ',', 'question.order', ',', 'questionnaire.is_draft', ',', 'response_files.count()')
for theme in Theme.objects.all():
    for index,question in enumerate(theme.questions.all()):
        if(index != question.order):
            print('Question', question.id, ', theme', theme.id, ', questionnaire', theme.questionnaire.id,': index', index, '- order', question.order, ': draft?', question.theme.questionnaire.is_draft, '- uploaded files', question.response_files.count())
            count = count + 1
print('Number of bad questions :', count)


# 1B. Lister les questions mal numerotées : format CSV
count = 0
print('question.id', ',', 'theme.id', ',', 'questionnaire.id', ',', 'index', ',', 'question.order', ',', 'questionnaire.is_draft', ',', 'response_files.count()')
for theme in Theme.objects.all():
    for index,question in enumerate(theme.questions.all()):
        if(index != question.order):
            print(question.id, ',', theme.id, ',', theme.questionnaire.id, ',', index, ',', question.order, ',', question.theme.questionnaire.is_draft, ',', question.response_files.count())
            count = count + 1
print('Number of bad questions :', count)


# 2. Lister les questions mal numerotées dans les questionnaires brouillons
count = 0
for theme in Theme.objects.filter(questionnaire__is_draft=True):
    for index,question in enumerate(theme.questions.all()):
        if(index != question.order):
            print('Question', question.id, ', theme', theme.id, ', questionnaire', theme.questionnaire.id,': index', index, '- order', question.order, ': draft?', question.theme.questionnaire.is_draft, '- uploaded files', question.response_files.count())
            count = count + 1
print('Number of bad questions :', count)


# 2B. Fixer les questions mal numerotées dans les questionnaires brouillons
count = 0
for theme in Theme.objects.filter(questionnaire__is_draft=True):
    for index,question in enumerate(theme.questions.all()):
        if(index != question.order):
            print('Question', question.id, ', theme', theme.id, ', questionnaire', theme.questionnaire.id,': index', index, '- order', question.order, ': draft?', question.theme.questionnaire.is_draft, '- uploaded files', question.response_files.count())
            question.order = index
            question.save()
            count = count + 1
print('Number of bad questions :', count)


# 3. Lister les questions mal numerotées dans les questionnaires publiés, qui n'ont pas de réponses déposées dans le theme
count = 0
for theme in Theme.objects.filter(questionnaire__is_draft=False):
    has_responses = False
    for index,question in enumerate(theme.questions.all()):
        if (question.response_files.count() > 0):
            has_responses = True
            break
    if has_responses:
        continue
    for index,question in enumerate(theme.questions.all()):
        if(index != question.order):
            print('Question', question.id, ', theme', theme.id, ', questionnaire', theme.questionnaire.id,': index', index, '- order', question.order, ': draft?', question.theme.questionnaire.is_draft, '- uploaded files', question.response_files.count())
            count = count + 1
print('Number of bad questions :', count)


# 3B. Fixer les questions mal numerotées dans les questionnaires publiés, qui n'ont pas de réponses déposées dans le theme
count = 0
for theme in Theme.objects.filter(questionnaire__is_draft=False):
    has_responses = False
    for index,question in enumerate(theme.questions.all()):
        if (question.response_files.count() > 0):
            has_responses = True
            break
    if has_responses:
        continue
    for index,question in enumerate(theme.questions.all()):
        if(index != question.order):
            print('Question', question.id, ', theme', theme.id, ', questionnaire', theme.questionnaire.id,': index', index, '- order', question.order, ': draft?', question.theme.questionnaire.is_draft, '- uploaded files', question.response_files.count())
            question.order = index
            question.save()
            count = count + 1
print('Number of bad questions :', count)


# 4. Lister les questions mal numerotées dans les questionnaires publiés, qui ont des réponses déposées dans le theme
question_count = 0
for theme in Theme.objects.filter(questionnaire__is_draft=False):
    has_responses = False
    for index,question in enumerate(theme.questions.all()):
        if (question.response_files.count() > 0):
            has_responses = True
            break
    if not has_responses:
        continue
    for index,question in enumerate(theme.questions.all()):
        if(index != question.order):
            print('Question', question.id, ', theme', theme.id, ', questionnaire', theme.questionnaire.id,': index', index, '- order', question.order, ': draft?', question.theme.questionnaire.is_draft, '- uploaded files', question.response_files.count())
            question_count = question_count + 1
print('Number of bad questions :', question_count)

# 4B. (CSV) Lister les questions mal numerotées dans les questionnaires publiés, qui ont des réponses déposées dans le theme
question_count = 0
print('question.id', '\t', 'theme.id', '\t', 'questionnaire.id', '\t', 'index', '\t', 'question.order', '\t', 'questionnaire.is_draft', '\t', 'question.response_files.count()')
for theme in Theme.objects.filter(questionnaire__is_draft=False):
    has_responses = False
    for index,question in enumerate(theme.questions.all()):
        if (question.response_files.count() > 0):
            has_responses = True
            break
    if not has_responses:
        continue
    for index,question in enumerate(theme.questions.all()):
        if(index != question.order):
            print(question.id, '\t', theme.id, '\t', theme.questionnaire.id, '\t', index, '\t', question.order, '\t', question.theme.questionnaire.is_draft, '\t', question.response_files.count())
            question_count = question_count + 1
print('Number of bad questions :', question_count)
