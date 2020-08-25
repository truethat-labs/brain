import pdb
import glob
import json
import os
import ast
import csv
# import pandas as pd
# import numpy as np

from ..helpers.stoploss import Stoploss
from ..helpers.order_outcome import OrderOutcome

from datetime import datetime
from itertools import groupby
from iteration_utilities import deepflatten

breakouts = []
# creating directory for storing Result
storeDir = "data/backtest/orb/"
if not os.path.exists(storeDir):  # If directory doesn't exit create new
    os.makedirs(storeDir)

path = r"data/structured/nff/minute"  # File path
DATE, OPEN, HIGH, LOW, CLOSE, VOLUME = 0, 1, 2, 3, 4, 5

# Sorting datewise of the file name that we have
dateName = sorted([datetime.strptime(x.replace('.json', ''),
                                     '%d-%m-%Y') for x in os.listdir(path)])
for date in dateName:
    # finding minimun date
    date = datetime.strptime(
        str(date), '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')

    # that date of file we fetching from directory we have
    with open(path+'/'+date+'.json', 'r') as f:
        if os.path.getsize(path+'/'+date+'.json') < 3:
            print("Empty file", date)
        else:
            distros_dict = json.load(f)  # Reading JSON file
            first15Minutes = distros_dict[0:15]  # First 15minutes data
            # Maximum value of HIGH in first 15 minutes
            high = float(max([data[HIGH] for data in first15Minutes]))
            # Minimum value of LOW in first 15 minutes
            low = float(min([data[LOW] for data in first15Minutes]))
            # target in percentage 1%
            target = 0.75
            # Stoploss in percentage 0.5%
            stoploss = 0.5
            orbStoploss = Stoploss()
            orbStopLossResult = orbStoploss.orbStoploss(high, low, target, stoploss) # high is buyBreakout and low is sellBreakout
            breakoutData = {
                'currDay': date,
                'buyBreakout': high,
                'sellBreakout': low,
                'buyStoploss': round(high - orbStopLossResult['buySl'], 2),
                'sellStoploss': round(low + orbStopLossResult['sellSl'], 2),
                'buyTarget': round(high + orbStopLossResult['buyTarget'], 2),
                'sellTarget': round(low - orbStopLossResult['sellTarget'], 2)
            }
            minutesData = distros_dict[15:-10]
            orderOutcome = OrderOutcome()
            orderOutcomeResult = orderOutcome.get(minutesData, breakoutData)
            
            if orderOutcomeResult != None:
                breakouts.append({**breakoutData, **orderOutcomeResult})

# create a csv file
with open('data/backtest/orb/nff_orb(with profit=0.75%, stoploss=0.5%).csv', 'w') as csvFile:
    fieldnames = ['currDay', 'buyBreakout', 'sellBreakout', 'buyStoploss', 'sellStoploss', 'buyTarget', 'sellTarget', 'call_type', 'profit_loss', 'pl_percentage']
    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(breakouts)

print("ALL DONE")