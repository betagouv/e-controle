import csv
import xlsxwriter

from tempfile import NamedTemporaryFile

HEADER = [
          'Thème (numéro)',
          'Thème (titre)',
          'Question (numéro)',
          'Nom du fichier',
          'Horodatage de dépôt',
          'Horodatage de dépôt, format triable par ordre chronologique',
          'Personne qui a déposé',
        ]

def generate_response_file_list_in_csv(questionnaire):
    """
    This creates a temp file. Delete it when you are done with it.
    """
    with NamedTemporaryFile(delete=False, mode='w') as f:
        csvwriter = csv.writer(f, quoting=csv.QUOTE_ALL)
        csvwriter.writerow(HEADER)
        for theme in questionnaire.themes.all():
            for question in theme.questions.all():
                for file in question.response_files.all():
                    csvwriter.writerow([
                      theme.numbering,
                      theme.title,
                      f'{theme.numbering}.{question.numbering}',
                      file.basename,
                      file.created.strftime('%a %d %B %Y à %X'),
                      file.created.strftime('%Y-%m-%d %H:%M:%S'),
                      f'{file.author.first_name} {file.author.last_name}'
                    ])

        return f


def generate_response_file_list_in_xlsx(questionnaire):
    # todo write function like write_and_increment_counter
    with NamedTemporaryFile(delete=False, mode='w') as f:
        with xlsxwriter.Workbook(f.name, {'remove_timezone': True}) as workbook:
            worksheet = workbook.add_worksheet()
            rowCounter = 0

            worksheet.write_row(rowCounter, 0, HEADER)
            rowCounter += 1
            # todo set row width for readability

            for theme in questionnaire.themes.all():
                for question in theme.questions.all():
                    for file in question.response_files.all():
                        worksheet.write_row(
                          rowCounter,
                          0,
                          [
                            theme.numbering,
                            theme.title,
                            f'{theme.numbering}.{question.numbering}',
                            file.basename,
                            file.created.strftime('%a %d %B %Y à %X'),
                            file.created.strftime('%Y-%m-%d %H:%M:%S'),
                            f'{file.author.first_name} {file.author.last_name}'
                          ])
                        rowCounter += 1

        return f
