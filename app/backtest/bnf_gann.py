# This is where bnf backtest will be done
# we will see which level gives decent accuracy and risk-reward ratio
# loop through all the dates of bank nifty futures f1
# get gann values from app.strategies.bnf_gann and push that to a list for levels (1, 2, 3)
# loop through the list and get the result for each item
# group by levels
# pass those grouped data to result.summary
# push grouped values to a csv with result
# summary will print everything
# push result at the end of the csv

import pdb # pdb.set_trace()
import json
import csv
import numpy as np
from datetime import datetime
from app.helpers.gann import Gann
from app.helpers.result import Result

DAYSYM, DAYDATE, DAYEXP, DAYOPEN, DAYHIGH, DAYLOW, DAYCLOSE, DAYVOLUME = 0, 1, 2, 3, 4, 5, 6, 7
MINDATE, MINOPEN, MINHIGH, MINLOW, MINCLOSE, MINVOL = 0, 1, 2, 3, 4, 5

with open('data/structured/bnf/bank_nifty_f1.json') as f:
    allDayData = json.load(f)

orders = []

for idx, dayData in enumerate(allDayData):
    openPrice = dayData[DAYOPEN]
    gann = Gann()
    gannValues = gann.squareOfNine(openPrice)
    date = datetime.strftime(datetime.strptime(dayData[DAYDATE], '%Y-%m-%d %H:%M:%S %z'), '%d-%m-%Y')

    # Level 1
    orders.append({
      "date": date,
      "buyBreakout": gannValues['buy_above'][1],
      "sellBreakout": gannValues['sell_below'][1],
      "buyStoploss": gannValues['sell_below'][1],
      "sellStoploss": gannValues['buy_above'][1],
      "buyTarget": gannValues['buy_above'][2],
      "sellTarget": gannValues['sell_below'][2],
      "quantity": 40,
      "level": 1
    })
    # Level 2
    orders.append({
      "date": date,
      "buyBreakout": gannValues['buy_above'][1],
      "sellBreakout": gannValues['sell_below'][1],
      "buyStoploss": gannValues['sell_below'][1],
      "sellStoploss": gannValues['buy_above'][1],
      "buyTarget": gannValues['buy_above'][3],
      "sellTarget": gannValues['sell_below'][3],
      "quantity": 40,
      "level": 2
    })
    # Level 3
    orders.append({
      "date": date,
      "buyBreakout": gannValues['buy_above'][1],
      "sellBreakout": gannValues['sell_below'][1],
      "buyStoploss": gannValues['sell_below'][1],
      "sellStoploss": gannValues['buy_above'][1],
      "buyTarget": gannValues['buy_above'][4],
      "sellTarget": gannValues['sell_below'][4],
      "quantity": 40,
      "level": 3
    })

for idx, order in enumerate(orders):
    result = Result()
    date = order['date']
    try:
        with open('data/structured/bnf/minute/'+ date +'.json') as f:
            minutesData = json.load(f)
        if len(minutesData) > 0:
            firstMinutes = minutesData[0:1]
            # highs = []
            # lows = []
            # for imin, min in enumerate(firstMinutes):
            #     highs.append(float(min[MINHIGH]))
            #     lows.append(float(min[MINLOW]))
            # high = np.array(highs).max()
            # low = np.array(lows).min()
            # pdb.set_trace()
            requiredMinutesData = minutesData[1:-11]
        if len(minutesData) > 0 and float(minutesData[0][MINCLOSE]) < order['buyBreakout'] and float(minutesData[0][MINCLOSE]) > order['sellBreakout']:
            response = result.get(requiredMinutesData, order)
            if response:
                orders[idx].update(response)
    except FileNotFoundError:
        print("Wrong file or file path")



with open('data/backtest/bnf_gann.csv', 'w') as csvFile:
    fieldnames = ['date', 'buyBreakout', 'sellBreakout', 'buyStoploss', 'sellStoploss', 'buyTarget', 'sellTarget', 'quantity', 'level', 'callSide', 'resultType', 'resultPoint']
    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(orders)
