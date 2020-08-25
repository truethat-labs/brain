import pdb
import glob
import json
import os
import ast
import csv
# import pandas as pd
# import numpy as np

from ..helpers.stoploss import Stoploss
from ..helpers.result import Result

from datetime import datetime
from itertools import groupby
from iteration_utilities import deepflatten

# target in percentage 1%
targetPercent = 1

breakouts = []
# creating directory for storing Result
storeDir = "data/backtest/bnf_nr/"
if not os.path.exists(storeDir):  # If directory doesn't exit create new
    os.makedirs(storeDir)

path = r"data/structured/bnf/minute"  # File path
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
            minuteData = json.load(f)  # Reading JSON file
            first15Minutes = minuteData[0:15]  # First 15minutes data
            # Maximum value of HIGH in first 15 minutes
            high = float(max([data[HIGH] for data in first15Minutes]))
            # Minimum value of LOW in first 15 minutes
            low = float(min([data[LOW] for data in first15Minutes]))

            openPrice = float(first15Minutes[0][OPEN])

            if (openPrice == low) | (openPrice == high):
                orbStoploss = Stoploss()
                
                rangePercent = ((high-low)/high)*100
                if rangePercent <= 0.5:
                    stoploss = rangePercent
                else:
                    stoploss = 0.5

                if openPrice == low:
                    callSide = "buy"
                    buyBreakout = high
                    sellBreakout = -80000
                    orbStopLossResult = orbStoploss.orbStoplossNr(buyBreakout, sellBreakout ,targetPercent, stoploss)
                if openPrice == high:
                    callSide = "sell"
                    sellBreakout = low
                    buyBreakout = 80000
                    orbStopLossResult = orbStoploss.orbStoplossNr(buyBreakout, sellBreakout, targetPercent, stoploss)
                                
                breakoutData = {
                    'currDay': date,
                    'openPrice': openPrice,
                    'buyBreakout': buyBreakout,
                    'sellBreakout': sellBreakout,
                    'buyStoploss': round(buyBreakout - orbStopLossResult['buySl'], 2),
                    'sellStoploss': round(sellBreakout + orbStopLossResult['sellSl'], 2),
                    'buyTarget': round(buyBreakout + orbStopLossResult['buyTarget'], 2),
                    'sellTarget': round(sellBreakout - orbStopLossResult['sellTarget'], 2),
                    "callSide": callSide
                }
                minutesData = minuteData[16:-15]
                result = Result()
                orbResult = result.get(minutesData, breakoutData)

                if orbResult != None:

                    # For correct price update to verify
                    orbStopLossResult = orbStoploss.orbStoplossNr(high, low ,targetPercent, stoploss)
                    breakoutData = {
                            'currDay': date,
                            'openPrice': openPrice,
                            'buyBreakout': high,
                            'sellBreakout': low,
                            'buyStoploss': round(high - orbStopLossResult['buySl'], 2),
                            'sellStoploss': round(low + orbStopLossResult['sellSl'], 2),
                            'buyTarget': round(high + orbStopLossResult['buyTarget'], 2),
                            'sellTarget': round(low - orbStopLossResult['sellTarget'], 2)
                            # "callSide": callSide
                        }
                    breakouts.append({**breakoutData, **orbResult})

# create a csv file
with open('data/backtest/bnf_nr/bnf_nr(target='+str(targetPercent)+').csv', 'w') as csvFile:
    fieldnames = ['currDay', 'openPrice', 'buyBreakout', 'sellBreakout', 'buyStoploss', 'sellStoploss',
                  'buyTarget', 'sellTarget', 'callSide', 'resultType', 'resultPoint']
    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(breakouts)

print("ALL DONE")
