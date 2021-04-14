import xlsxwriter

from datetime import date
from .models import ResponseFile
from tempfile import NamedTemporaryFile


def get_files_for_export(questionnaire):
    queryset = ResponseFile.objects \
            .filter(question__theme__questionnaire=questionnaire) \
            .filter(is_deleted=False) \
            .order_by('question__theme__numbering', 'question__numbering', 'created') \
            .all()
    return queryset


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
            add_row(worksheet, ['Fichier publié le',
                                questionnaire.sent_date_display])
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

            data = [
                (
                    file.question.theme.numbering,
                    file.question.theme.title,
                    f"{file.theme.numbering}.{file.question.numbering}",
                    file.question.description,
                    file.basename,
                    f"{file.author.first_name} {file.author.last_name}",
                    file.created.strftime('%Y-%m-%d'),
                    file.created.strftime('%H:%M:%S')
                )
                for file in get_files_for_export(questionnaire)
            ]

            opts = {
                'data': data,
                'columns': columns
            }

            table_size = f'A11:I{len(data) + 11}'
            worksheet.add_table(table_size, opts)

        return f
