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


################# START ###########################
# For changes here to Enter:
capital = 20000  # Capital in Rupies 20,000 ex: capital = 20000
target = 1.7  # target in percentage 1%

# (buybreakout - sellbreakout)range in percentage ex: rangeFrom = 1 is 1%, ex: rangeTo=1.5 is 1.5%
rangeFrom = 1
rangeTo = 1.4

# for top 5 stock ex: sortedSym = 'top5', for bottom 5 stock ex: sortedSym = 'bottom5'
sortingSymbol = 'top5'
################# End #############################


# To store final result path and name
resultSheetPath = 'data/backtest/orb_nr/orb_nr(' + sortingSymbol + ',range=' + str(
    rangeFrom) + '-' + str(rangeTo) + '%, target=' + str(target) + '%, capital=' + str(capital) + ').csv'

filePath = r"data/structured/fno/minutes/"  # File path for minute directory
# symbols = pd.read_json("data/structured/symbols.json", typ='series').keys() # symbols all 208
symbols = pd.read_json("data/structured/good_price_symbols.json",
                       typ='series').keys()  # only Good price symbols
noUseStocks = pd.read_csv('data/structured/fno/no_use_stocks.txt',
                          header=None).values  # No use stock Symbols

DATE, OPEN, HIGH, LOW, CLOSE, VOLUME = 0, 1, 2, 3, 4, 5

breakouts = []
# creating directory for storing Result
storeDir = "data/backtest/orb_nr/"
if not os.path.exists(storeDir):  # If directory doesn't exit create new
    os.makedirs(storeDir)

missingsym = []

# Filter symbol only that usefull
UseSymbols = []
for symbol in symbols:
    if symbol in noUseStocks:
        print("Reject: ", symbol)
    else:
        UseSymbols.append(symbol)

# Sorting datewise of the file name that we have
dateName = []
for symbol in UseSymbols:
    fullPath = os.path.join(filePath, symbol)
    if os.path.isdir(fullPath):
        dateName.append(sorted([datetime.strptime(
            x.replace('.json', ''), '%d-%m-%Y') for x in os.listdir(fullPath)]))

dateName = sorted(set(np.array(dateName).flatten()))
for date in dateName:
    date = datetime.strptime(
        str(date), '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')

    curDaySym = []
    for symbol in UseSymbols:
        fullPath = os.path.join(filePath, symbol)
        if os.path.isfile(fullPath+'/'+date+".json"):
            with open(fullPath+'/'+date+'.json', 'r') as f:
                minuteData = json.load(f)  # Reading JSON file

                # check file has empty array or not
                if os.path.getsize(fullPath+'/'+date+'.json') > 2:
                    first15Minutes = minuteData[0:15]  # First 15minutes data
                    # Maximum value of HIGH in first 15 minutes
                    high = float(max([data[HIGH] for data in first15Minutes]))
                    # Minimum value of LOW in first 15 minutes
                    low = float(min([data[LOW] for data in first15Minutes]))
                    if high <= 10000:  # Check price exceeds 10000
                        rangePercent = ((high-low)/high)*100
                        if (rangePercent >= rangeFrom) & (rangePercent <= rangeTo):
                            data = {
                                'symbol': symbol,
                                'rangePercent': rangePercent,
                                'buyBreakout': high,
                                'sellBreakout': low
                            }
                            curDaySym.append(data)
                        # else:
                        #     print("Range Percentage reject",
                        #           rangePercent, symbol)
                    # else:
                    #     print("Price exceeds 10000: ",symbol)

    if len(curDaySym) > 0:
        curDaySym = pd.DataFrame(curDaySym)
        if sortingSymbol == 'top5':
            sortedSym = curDaySym.sort_values(
                by=['rangePercent'], ascending=False)[0:5]  # Top 5
        elif sortingSymbol == 'bottom5':
            sortedSym = curDaySym.sort_values(
                by=['rangePercent'])[0:5]  # Bottom5
        for symbolData in sortedSym.values:
            symbol = symbolData[3]
            buyBreakout = symbolData[0]
            sellBreakout = symbolData[2]
            rangePercent = symbolData[1]
            orbNrStoploss = Stoploss()
            # high is buyBreakout and low is sellBreakout
            stopLossResult = orbNrStoploss.orbNrStoploss(
                buyBreakout, sellBreakout, capital, target)
            breakoutData = {
                'currDay': date,
                'symbol': symbol,
                'range': rangePercent,
                'buyBreakout': buyBreakout,
                'sellBreakout': sellBreakout,
                'buyStoploss': round(buyBreakout - stopLossResult['buySl'], 2),
                'sellStoploss': round(sellBreakout + stopLossResult['sellSl'], 2),
                'buyTarget': round(buyBreakout + stopLossResult['buyTarget'], 2),
                'sellTarget': round(sellBreakout - stopLossResult['sellTarget'], 2),
                'qty': stopLossResult['qty']
            }
            with open(filePath+symbol+'/'+date+'.json', 'r') as f:
                minuteData = json.load(f)  # Reading JSON file
            # minute data from time 9:31 to 3:20
            minuteData = minuteData[15:-15]
            result = Result()
            orbNrResult = result.get(minuteData, breakoutData)

            if orbNrResult != None:
                orbNrResult = {
                    'callSide': orbNrResult['callSide'],
                    'resultType': orbNrResult['resultType'],
                    'resultPoint': round((breakoutData['qty'] * orbNrResult['resultPoint']), 2),
                }
                breakouts.append({**breakoutData, **orbNrResult})
        print("Complted Date: ",date)

# create a csv file
with open(resultSheetPath, 'w') as csvFile:
    fieldnames = ['currDay', 'symbol', 'range', 'buyBreakout', 'sellBreakout', 'buyStoploss', 'sellStoploss',
                  'buyTarget', 'sellTarget', 'qty', 'callSide', 'resultType', 'resultPoint']
    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(breakouts)

print("See Result: ", resultSheetPath)
print("ALL DONE")
