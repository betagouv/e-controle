import csv
import xlsxwriter

from datetime import date
from tempfile import NamedTemporaryFile

HEADER = [
          'N° de thème',
          'Thème',
          'N° de question',
          'Question',
          'Nom du fichier',
          'Déposé par',
          'Horodatage de dépôt',
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
        return row_counter - 1

    with NamedTemporaryFile(delete=False, mode='w') as f:
        with xlsxwriter.Workbook(f.name, {'remove_timezone': True}) as workbook:
            worksheet = workbook.add_worksheet()

            add_row(worksheet, [ f'Organisme : { questionnaire.control.depositing_organization}' ])
            add_row(worksheet, [ f'Procédure : { questionnaire.control.title}' ])
            add_row(worksheet, [ f'Dossier : /{ questionnaire.control.reference_code}' ])
            add_row(worksheet, [])
            add_row(worksheet, [ f'Questionnaire { questionnaire.numbering } : { questionnaire.title}' ])
            if questionnaire.end_date:
                add_row(worksheet, [ f'Date limite de dépôt : { questionnaire.end_date_display }' ])
            add_row(worksheet, [ f'Exporté le : { date.today().strftime("%A %d %B %Y") }' ])
            add_row(worksheet, [])

            header_row = add_row(worksheet, HEADER)
            # Set row widths
            worksheet.set_column(1, 1, 30)
            worksheet.set_column(3, 6, 30)
            # Set text wrapping for headers
            worksheet.set_row(header_row, None, workbook.add_format({'text_wrap': True}))

            for theme in questionnaire.themes.all():
                for question in theme.questions.all():
                    for file in question.response_files.all():
                        add_row(
                          worksheet,
                          [
                            theme.numbering,
                            theme.title,
                            f'{theme.numbering}.{question.numbering}',
                            question.description,
                            file.basename,
                            f'{file.author.first_name} {file.author.last_name}',
                            file.created.strftime('%Y-%m-%d %H:%M:%S')
                          ])

        return f
