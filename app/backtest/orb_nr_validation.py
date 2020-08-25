import pdb
import os
import json
import csv
import pandas as pd
import numpy as np

csvFile = pd.read_csv('data/backtest/orb_nr/orb_nr_validation.csv', sep=',',header=None)
# pdb.set_trace()
csvFile.values[1:]
maxDrawdown = 0
drawDown = 0
drawDownCount = 0

maxProfit = 0
profit = 0
profitCount = 0

print("Preparing...")
for data in csvFile.values[1:]:
  # pdb.set_trace()
  data[-1] = float(data[-1])
  if data[-1]<=0:
    drawDownCount = drawDownCount + 1
    drawDown = drawDown + data[-1]
  if drawDown < maxDrawdown:
    maxDrawdown = drawDown
  if data[-1]>0:
    drawDownCount = 0
    drawDown = 0
  # print("Drawdown", maxDrawdown,"drawDown", drawDown,"drawDownCount", drawDownCount)

  if data[-1]>0:
    profitCount = profitCount + 1
    profit = profit + data[-1]
  if profit > maxProfit:
    maxProfit = profit
  if data[-1]<0:
    profitCount = 0
    profit = 0
  # pdb.set_trace()
print("Final: Max DrawDown", maxDrawdown)
print("Final: Max Profit", maxProfit)
