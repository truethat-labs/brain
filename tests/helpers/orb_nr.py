import pdb
import os
import json
import csv
import pandas as pd
from datetime import datetime
from os import walk
from os.path import isfile
from itertools import groupby
DATE, OPEN, HIGH, LOW, CLOSE, VOLUME = 0, 1, 2, 3, 4, 5

############################################
# Testing:
# Range is not between 0.5 to 1.5
with open('tests/data/fno/minutes/range_satisfy.json') as f:
    minutes = json.load(f)

first15Minutes = minutes[0:15]  # First 15minutes data
# Maximum value of HIGH in first 15 minutes
high = float(max([data[HIGH] for data in first15Minutes]))
# Minimum value of LOW in first 15 minutes
low = float(min([data[LOW] for data in first15Minutes]))
rangePercent = ((high-low)/high)*100
if (rangePercent <= 1.5) & (rangePercent >= 0.5):
    print('PASSED: Range between 0.5 to 1.5')
else:
    print('FAILED: Range not in betweem 0.5 to 1.5')
