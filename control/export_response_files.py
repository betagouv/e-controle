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
        csvwriter.writerow([
          '1',
          'Comptabilité',
          '1.2',
          'fichier1.pdf',
          'Mer 13 mai 2020 à 16:09:33',
          '2020-05-13T16:09:33.595213+02:00',
          'Julie Delacour'
        ])
        return f
    # todo delete temp file when we are done
