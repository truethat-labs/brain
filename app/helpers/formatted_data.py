import pdb
import os
import json
import math
import pandas as pd
from datetime import datetime, timedelta

DATE, OPEN, HIGH, LOW, CLOSE, VOLUME = 0, 1, 2, 3, 4, 5

# Naked Object
class Symbol(object):
    pass

# Naked Object
class MinuteData(object):
    pass
  
# Naked Object
class OHLCV(object):
    pass

class FormattedData:
    # Get a start date and end date, create list of all dates in the range
    def dateRange(self, startDate, endDate):
      sdate = datetime.strptime(startDate, '%Y-%m-%d')
      edate = datetime.strptime(endDate, '%Y-%m-%d')
      return pd.date_range(sdate, edate-timedelta(days=1), freq='d')
    
    # Map the data to Date, OHLC, Volume for easy access
    def ohlcv(self, item):
      ohlcvData = OHLCV()
      ohlcvData.date = item[0]
      ohlcvData.open = item[1]
      ohlcvData.high = item[2]
      ohlcvData.low = item[3]
      ohlcvData.close = item[4]
      ohlcvData.volume = item[5]
      return ohlcvData

    # Get all symbols data
    # day & minutes for the given date range
    def all(self):
      symbols = self.symbols()
      data = []

      for symbol in symbols:
        symbolData = Symbol()
        symbolData.name = symbol
        symbolData.days = self.dayData(symbol)
        symbolData.minutes = self.minuteData(symbol)
        data.append(symbolData)
      return data

    # Get all data of a given symbol
    # day & minutes for given date range
    def get(self, symbol):
      symbolData = Symbol()
      symbolData.name = symbol
      symbolData.days = self.dayData(symbol)
      symbolData.minutes = self.minuteData(symbol)
      return symbolData

    # Get all symbols in an list
    def symbols(self):
      symbols = pd.read_json("data/structured/symbols.json", typ='series').keys()
      return symbols

    # Get day data of a given sumbol
    def dayData(self, symbol):
      filePathDayData = r"data/structured/fno/day/"
      return self.daySymbolData(filePathDayData, symbol)

    # Helper for self.dayData()
    def daySymbolData(self, path, symbol):
      dayData = []
      if os.path.isfile(path+'/'+symbol+".json"):
          with open(path+'/'+symbol+'.json', 'r') as f:
              dayData = json.load(f)
      
      ohlcMapped = []
      for item in dayData:
        ohlcMapped.append(self.ohlcv(item))

      return ohlcMapped

    # Path to minutes data folder
    def filePathMinutesData(self):
      return r"data/structured/fno/minutes/"
    
    # Get all minutes data for a given symbol
    def minuteData(self, symbol):
      return self.allMinuteSymbolData(symbol)
    
    # Helper for self.minuteData()
    def allMinuteSymbolData(self, symbol):
      dates = self.dateRange('2017-01-01', '2019-12-31')
      data = []
      for date in dates:
        minuteData = self.dateMinuteSymbolData(symbol, date)
        if minuteData is not None:
          data.append(minuteData)
      return data
    
    # Get data for a specific symbol for a given date
    def dateMinuteSymbolData(self, symbol, date):
      fullMinutesPath = os.path.join(self.filePathMinutesData(), symbol)
      dateStr = date.date().strftime('%d-%m-%Y')
      dayMinuteData = []
      if os.path.isfile(fullMinutesPath+'/'+dateStr+".json"):
            with open(fullMinutesPath+'/'+dateStr+'.json', 'r') as f:
                dayMinuteData.append(date.date())
                minuteData = json.load(f)

                ohlcMapped = []
                for item in minuteData:
                  ohlcMapped.append(self.ohlcv(item))

                dayMinuteData.append(ohlcMapped)

      return dayMinuteData if len(dayMinuteData) else None
