# Example Strategy

import pdb
import os
import json
import csv
import pandas as pd
import numpy as np
from datetime import datetime
from os import walk
from os.path import isfile
from itertools import groupby

from ..helpers.stoploss import Stoploss
from ..helpers.result import Result
from ..helpers.formatted_data import FormattedData

filePath = r"data/structured/fno/minutes/"  # File path for minute directory
symbols = pd.read_json("data/structured/symbols.json", typ='series').keys() # symbols all 208

DATE, OPEN, HIGH, LOW, CLOSE, VOLUME = 0, 1, 2, 3, 4, 5

formattedData = FormattedData()
data = formattedData.get('ACC')
