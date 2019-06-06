"""
This is a one time bugfix reorder the numbering and rename file.

    ./manage.py shell_plus
    from utils.bugfix_order import *

    check_files()  # Fix issues if any
    fix_ordering() # Check in the admin that the ordering is fixed
    fix_files()    # Check in webdan that files are reorganized
"""

import os
import shutil

from control.models import ResponseFile, Questionnaire
from django.core.files import File

CONTROL_TITLE = 'Contrôle des comptes et de la gestion de la commune de TODO'
Q1_TITLE = 'Questionnaire n°1 - présentation générale - TODO'
Q2_TITLE = 'Questionnaire n°2 - Fiabilité des comptes - TODO'
Q3_TITLE = 'Questionnaire n°3 - Gestion des ressources humaines - TODO'


def fix_ordering():
    q1 = Questionnaire.objects.get(title=Q1_TITLE)
    q1.order = 0
    q1.save()

    q2 = Questionnaire.objects.get(title=Q2_TITLE)
    q2.order = 1
    q2.save()

    q3 = Questionnaire.objects.get(title=Q3_TITLE)
    q3.order = 2
    q3.save()


def fix_files():
    response_files = ResponseFile.objects.filter(
        question__theme__questionnaire__control__title=CONTROL_TITLE)
    for rfile in response_files:
        old_file_filed = rfile.file
        old_file_object = old_file_filed.file
        clean_basename = rfile.strip_prefix(rfile.basename)
        new_file_object = File(file=old_file_object, name=clean_basename)
        rfile.file = new_file_object
        rfile.save()
        backup_file_name = '/tmp/backup-vj/' + os.path.basename(old_file_object.name)
        if os.path.isfile(old_file_filed.path):
            shutil.move(old_file_object.name, backup_file_name)


def check_files():
    response_files = ResponseFile.objects.filter(
        question__theme__questionnaire__control__title=CONTROL_TITLE)
    for rfile in response_files:
        if os.path.isfile(rfile.file.path):
            print(rfile)
        else:
            raise Exception(f"ERROR : no file for {rfile}")
