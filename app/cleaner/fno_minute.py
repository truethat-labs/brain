import pdb
import os
import json
import csv
import pandas as pd
from datetime import datetime
from os import walk
from os.path import isfile
from itertools import groupby

filePath = r"data/unstructured/IntradayData_2018/"  # File path
symbols = pd.read_json("data/structured/symbols.json", typ='series').keys()
exitistingSymbol = []
missingDataSymbols = []
for symbol in symbols:
    allData = []
    fullPath = os.path.join(filePath, symbol)

    if os.path.isfile(fullPath+".txt"):
        exitistingSymbol.append(symbol) # Storing symbol in array which has data
        f = open(fullPath+".txt", 'r')
        fileData = csv.reader(f)
        for data in fileData:
            allData.append(data)
    else:
        missingDataSymbols.append(symbol) #Storing symbol in array which dont have data
        print("miutedata not there", symbol)

    groupData = [list(j) for i, j in groupby(allData, lambda item: item[1])]

    for dateData in groupData:
        minuteData = [x for x in dateData if x[2] > "09:15" and x[2] < "15:31"]

        # Arranging grouped data in the format "date,open,high,low,close,volume"
        arrangedData = []
        for data in minuteData:
            if len(data) == 7:  # Here we adding 0, if volume data not exist
                data.append('0')
                minData = [str(datetime.strptime(data[1]+data[2], '%Y%m%d%H:%M')),
                           data[3], data[4], data[5], data[6], data[7]]
                arrangedData.append(minData)
            else:  # if volume field exist
                minData = [str(datetime.strptime(data[1]+data[2], '%Y%m%d%H:%M')),
                           data[3], data[4], data[5], data[6], data[7]]
                arrangedData.append(minData)

        # Finding date for store in each date.json in the formate "date-month-year"
        date = datetime.strptime(dateData[0][1], '%Y%m%d').strftime('%d-%m-%Y')

        # creating directory for storing minute data
        baseDir = 'data/structured/fno/minute/' + symbol + '/'
        if not os.path.exists(baseDir):  # If directory doesn't exit create new
            os.makedirs(baseDir)

        # Here we creating a JSON file in datewise
        with open('data/structured/fno/minute/' + symbol + '/' + date + '.json', 'w') as outfile:
            json.dump(arrangedData, outfile, indent=2)
        print("File "+date+".json complete")

# print("missing data of symbols", missingDataSymbols)
print("total missing symbol : ", len(missingDataSymbols))
# print("exist data of symbols", exitistingSymbol)
print("total exist symbol : ", len(exitistingSymbol))
print("All Done...")


# for symbol in symbols:
#   fullPath = os.path.join(baseDir, symbol)
#   if os.path.isfile(fullPath+".txt"):
#     filesData = pd.read_csv(fullPath+".txt", header=None)
#     groupData = filesData.groupby(filesData[1])
#     for dayData in groupData:
#       dayData = dayData[1]
#       minuteData = dayData[(dayData[2] > "09:15") & (dayData[2] < "15:31")]

#       # Arranging grouped data in the format "date,open,high,low,close,volume"
#       arrangedData = []
#       for data in minuteData:
#           pdb.set_trace()

#     print("All Done")
#     # groupData = [list(j) for i, j in groupby(filesData, lambda item: item[1])]
#   else:
#     print("miutedata not there", +symbol)
#   # if(glob.glob(baseDir".txt")):
#   #   pdb.set_trace()