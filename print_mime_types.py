#!/usr/bin/env python3

import os
import subprocess
import sys
import csv

current_dir = os.getcwd()
csvwriter = csv.writer(sys.stdout)

for root, dirs, files in os.walk(current_dir):
    for name in files:
        file = root+"/"+name
        ftype = subprocess.check_output(['file', '--mime-type', '-b', file]).decode('utf-8').strip()
        csvwriter.writerow([ftype, file])

