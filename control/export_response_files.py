import csv
from tempfile import NamedTemporaryFile


def generate_response_file_list_in_csv(questionnaire):
    with NamedTemporaryFile(delete=False, mode='w') as f:
        csvwriter = csv.writer(f, quoting=csv.QUOTE_ALL)
        csvwriter.writerow([
          'Thème (numéro)',
          'Thème (titre)',
          'Question (numéro)',
          'Nom du fichier',
          'Horodatage de dépôt',
          'Horodatage de dépôt, format triable par ordre chronologique',
          'Personne qui a déposé',
        ])
        for theme in questionnaire.themes.all():
            for question in theme.questions.all():
                for file in question.response_files.all():
                    csvwriter.writerow([
                      theme.numbering,
                      theme.title,
                      f'{theme.numbering}.{question.numbering}',
                      file.basename,
                      file.created.strftime('%a %d %B %Y à %X'),
                      file.created,
                      f'{file.author.first_name} {file.author.last_name}'
                    ])

        return f
    # todo delete temp file when we are done
