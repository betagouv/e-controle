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
    row_counter = 0
    def add_row(worksheet, row_contents):
        nonlocal row_counter
        worksheet.write_row(row_counter, 0, row_contents)
        row_counter += 1

    with NamedTemporaryFile(delete=False, mode='w') as f:
        with xlsxwriter.Workbook(f.name, {'remove_timezone': True}) as workbook:
            worksheet = workbook.add_worksheet()
            worksheet.set_column(1, 1, 30)
            worksheet.set_column(3, 6, 30)
            worksheet.set_row(0, None, workbook.add_format({'text_wrap': True}))

            add_row(worksheet, HEADER)

            for theme in questionnaire.themes.all():
                for question in theme.questions.all():
                    for file in question.response_files.all():
                        add_row(
                          worksheet,
                          [
                            theme.numbering,
                            theme.title,
                            f'{theme.numbering}.{question.numbering}',
                            file.basename,
                            file.created.strftime('%a %d %B %Y à %X'),
                            file.created.strftime('%Y-%m-%d %H:%M:%S'),
                            f'{file.author.first_name} {file.author.last_name}'
                          ])

        return f
