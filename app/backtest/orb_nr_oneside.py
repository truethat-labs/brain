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

# for top 5 stock ex: sortedSym = 'top5', for bottom 5 stock ex: sortedSym = 'bottom5', ex:"all"
sortingSymbol = 'all'

# which side do
onesideType = 'reversebuy' # buy/sell/reversebuy/reversesell
################# End #############################

# To store final result path and name
resultSheetPath = 'data/backtest/orb_nr/orb_nr_oneside_'+ onesideType +'(' + sortingSymbol + ').csv'

# File path for minute directory
filePathMinutesData = r"data/structured/fno/minutes/"
filePathDayData = r"data/structured/fno/day/"  # File path day data
symbols = pd.read_json("data/structured/good_price_symbols.json",
                       typ='series').keys()  # only Good price symbols

DATE, OPEN, HIGH, LOW, CLOSE, VOLUME = 0, 1, 2, 3, 4, 5

breakouts = []
missingsym = []
# creating directory for storing Result
storeDir = "data/backtest/orb_nr/"
if not os.path.exists(storeDir):  # If directory doesn't exit create new
    os.makedirs(storeDir)


# Filter symbol only that usefull
UseSymbols = []
for symbol in symbols:
    # if symbol in onlyBuy:
    UseSymbols.append(symbol)

# Sorting ascending order of datewise of the files name
dateName = []
for symbol in UseSymbols:
    fullPath = os.path.join(filePathMinutesData, symbol)
    if os.path.isdir(fullPath):
        dateName.append(sorted([datetime.strptime(
            x.replace('.json', ''), '%d-%m-%Y') for x in os.listdir(fullPath)]))

dateName = sorted(set(np.array(dateName).flatten()))
for date in dateName:
    date = datetime.strptime(
        str(date), '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')

    curDaySym = []
    for symbol in UseSymbols:
        fullPath = os.path.join(filePathMinutesData, symbol)
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
        elif sortingSymbol == 'all':
            sortedSym = curDaySym.sort_values(
                by=['rangePercent'], ascending=False) # all symbols
        for symbolData in sortedSym.values:
            # level 1 change | here increasing 0.1 higher price because to execute order
            # Difference between buy and sell
            rangeDiff = abs(symbolData[0] - symbolData[2])
            
            # # If you need without 0.1 increment comment below 2 lines
            # symbolData[0] = symbolData[0] + 0.1
            # symbolData[2] = symbolData[2] - 0.1

            symbol = symbolData[3]
            rangePercent = symbolData[1]

            if ((onesideType == "buy") | (onesideType == "sell")):
                buyBreakout = symbolData[0]
                sellBreakout = symbolData[2]
                orbNrStoploss = Stoploss()
                stopLossResult = orbNrStoploss.orbNrStoploss(
                    buyBreakout, sellBreakout, rangeDiff, capital, target)

            # Here for reverse interchange breakout values
            elif ((onesideType == "reversebuy") | (onesideType == "reversesell")):
                buyBreakout = symbolData[2]
                sellBreakout = symbolData[0]
                orbNrStoploss = Stoploss()
                stopLossResult = orbNrStoploss.orbNrStoploss(
                    buyBreakout, sellBreakout, rangeDiff, capital, target)            

            # Fetch Day data 
            formatedDate = datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%dT00:00:00+0530')
            if os.path.isfile(filePathDayData+'/'+symbol+".json"):
                with open(filePathDayData+'/'+symbol+'.json', 'r') as f:
                    dayData = json.load(f)  # Reading JSON file

                dfDayData = pd.DataFrame(dayData).set_index(0)                

                dayOpen = dfDayData.loc[formatedDate][OPEN]
                dayHigh = dfDayData.loc[formatedDate][HIGH]
                dayLow = dfDayData.loc[formatedDate][LOW]
                dayClose = dfDayData.loc[formatedDate][CLOSE]
            else:
                dayOpen = '0'
                dayHigh = '0'
                dayLow = '0'
                dayClose = '0'
                print("day data not there")         
            
            breakoutDatacurrent = {
                'currDay': date,
                'symbol': symbol,
                'range': rangePercent,
                'open': dayOpen,
                'high': dayHigh,
                'low': dayLow,
                'close': dayClose,
                'buyBreakout': buyBreakout,
                'sellBreakout': sellBreakout,
                'buyStoploss': round(buyBreakout - stopLossResult['buySl'], 2),
                'sellStoploss': round(sellBreakout + stopLossResult['sellSl'], 2),
                'buyTarget': round(buyBreakout + stopLossResult['buyTarget'], 2),
                'sellTarget': round(sellBreakout - stopLossResult['sellTarget'], 2),
                'qty': stopLossResult['qty']
            }
            if ((onesideType == "buy")):
                sellBreakout = -50000
            elif ((onesideType == "sell")):
                buyBreakout = 50000
            elif ((onesideType == "reversebuy")):
                sellBreakout = 50000
            elif ((onesideType == "reversesell")):
                buyBreakout = -50000

            breakoutData = {
                'currDay': date,
                'symbol': symbol,
                'range': rangePercent,
                'open': dayOpen,
                'high': dayHigh,
                'low': dayLow,
                'close': dayClose,
                'buyBreakout': buyBreakout,
                'sellBreakout': sellBreakout,
                'buyStoploss': round(buyBreakout - stopLossResult['buySl'], 2),
                'sellStoploss': round(sellBreakout + stopLossResult['sellSl'], 2),
                'buyTarget': round(buyBreakout + stopLossResult['buyTarget'], 2),
                'sellTarget': round(sellBreakout - stopLossResult['sellTarget'], 2),
                'qty': stopLossResult['qty']
            }
            with open(filePathMinutesData+symbol+'/'+date+'.json', 'r') as f:
                minuteData = json.load(f)  # Reading JSON file
            # minute data from time 9:31 to 3:15
            minuteData = minuteData[16:-15]
            symbolStatus = onesideType
            if ((symbolStatus == "reversebuy") | (symbolStatus == "reversesell")):
                result = Result()
                orbNrResult = result.get(minuteData, breakoutData, "reverse")
            else:
                result = Result()
                orbNrResult = result.get(minuteData, breakoutData)

            if orbNrResult != None:
                orbNrResult = {
                    'behaviour': symbolStatus,
                    'callSide': orbNrResult['callSide'],
                    'resultType': orbNrResult['resultType'],
                    'resultPoint': round((breakoutData['qty'] * orbNrResult['resultPoint']), 2),
                }
                breakouts.append({**breakoutDatacurrent, **orbNrResult})
        print("Complted Date: ",date)

with open(resultSheetPath, 'w') as csvFile:
    fieldnames = ['currDay', 'symbol', 'range', 'open', 'high', 'low', 'close', 'buyBreakout', 'sellBreakout', 'buyStoploss', 'sellStoploss',
                  'buyTarget', 'sellTarget', 'qty', 'behaviour', 'callSide', 'resultType', 'resultPoint']
    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(breakouts)

print("See Result: ", resultSheetPath)
print("ALL DONE")
