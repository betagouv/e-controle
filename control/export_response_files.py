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

            add_row(worksheet, ['Organisme interrogé',
                                questionnaire.control.depositing_organization])
            add_row(worksheet, ['Procédure',
                                questionnaire.control.title])
            add_row(worksheet, ['Dossier',
                                f'/{questionnaire.control.reference_code}'])
            add_row(worksheet, ['Fichier exporté le',
                                date.today().strftime("%A %d %B %Y")])
            add_row(worksheet, [])
            add_row(worksheet, [])
            add_row(worksheet, ['Questionnaire',
                    f'Questionnaire {questionnaire.numbering } : { questionnaire.title }'])

            if questionnaire.end_date:
                add_row(worksheet, ['Date limite de réponse',
                                    questionnaire.end_date_display])
            add_row(worksheet, [])

            worksheet.set_column('A:L', 20)

            columns = [
                {'header': 'N° de Thème'},
                {'header': 'Thème'},
                {'header': 'N° de Question'},
                {'header': 'Question'},
                {'header': 'Fichiers déposés'},
                {'header': 'Déposé par'},
                {'header': 'Date de dépôt'},
                {'header': 'Heure de dépôt'},
                {'header': 'Commentaires'}
            ]

            table = [
                {
                    'theme': theme,
                    'question': question,
                    'file': file
                }
                for theme in questionnaire.themes.all()
                for question in theme.questions.all()
                for file in question.response_files.all()
            ]

            data = [(
                row['theme'].numbering,
                row['theme'].title,
                f"{row['theme'].numbering}.{row['question'].numbering}",
                row['question'].description,
                row['file'].basename,
                f"{row['file'].author.first_name} {row['file'].author.last_name}",
                row['file'].created.strftime('%Y-%m-%d'),
                row['file'].created.strftime('%H:%M:%S')
            )
                for row in table]

            opts = {
                'data': data,
                'columns': columns
            }

            table_size = f'A11:I{len(data) + 11}'
            worksheet.add_table(table_size, opts)

        return f
