import pdb
import os
import json
import csv
from datetime import datetime
from os import walk
from os.path import isfile
from itertools import groupby

# creating directory for storing minute data
baseDir = "data/structured/nspot/minute/"
if not os.path.exists(baseDir): # If directory doesn't exit create new
    os.makedirs(baseDir)

allData = []

# Fetching directory which have all data
filePath = r"data/unstructured/Backtest Data-20190102T054135Z-001/Backtest Data/Nifty 50 and BN SPOT - One Minute Data - 2008 - 2018/Consolidated"
print("Preparing please wait...")

# Fetching all the .txt file which ends with name " NIFTY.txt" inside the directory mentioned above and storing in a array
for root, dirs, files in os.walk(filePath):
    for file in files:
        if file.endswith(" NIFTY.txt"):
            rFile = os.path.join(root, file)
            f = open(rFile, 'r')
            fileData = csv.reader(f)
            for data in fileData:
                allData.append(data)

# Grouping the data in DATEWISE
groupData = [list(j) for i, j in groupby(allData, lambda item: item[1])]
for dateData in groupData:
    dateData.sort(key=lambda x: datetime.strptime(x[1], '%Y%m%d'))
    minuteData = [x for x in dateData if x[2] > "09:15" and x[2] < "15:31"]

    # Arranging grouped data in the format "date,open,high,low,close,volume"
    arrangedData = []
    for data in minuteData:
        if len(data) == 7:  # Here we adding 0, if volume data not exist
            data.append('0')
            minData = [str(datetime.strptime(data[1]+data[2], '%Y%m%d%H:%M')),
                       data[3], data[4], data[5], data[6], data[7]]
            arrangedData.append(minData)
        else:  # if volume fied exist
            minData = [str(datetime.strptime(data[1]+data[2], '%Y%m%d%H:%M')),
                       data[3], data[4], data[5], data[6], data[7]]
            arrangedData.append(minData)

    # Finding date for store in each date.json in the formate "date-month-year"
    date = datetime.strptime(dateData[0][1], '%Y%m%d').strftime('%d-%m-%Y')

    # Here we creating a JSON file in datewise
    with open('data/structured/nspot/minute/' + date + '.json', 'w') as outfile:
        json.dump(arrangedData, outfile, indent=2)
    print("File "+date+".json complete")

print("All Done")