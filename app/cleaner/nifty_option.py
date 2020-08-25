#############################################################
##########            NIFTY OPTION         ##################
#############################################################

import pdb
import os
import pandas as pd

baseDir = "data/structured/nifty_option/minute/"
pdb.set_trace()

# import pandas as pd
# import pdb
# import os
# import json
# import csv
# from datetime import datetime
# from os import walk
# from os.path import isfile
# from itertools import groupby

# baseDir = "data/structured/nifty_option/minute/"
# if not os.path.exists(baseDir):
#     os.makedirs(baseDir)

# allData = []
# filePath = r"data/unstructured/Backtest Data-20190102T054135Z-001/Backtest Data/Nfity Options One Minute Data"
# print("Preparing please wait...")
# for root, dirs, files in os.walk(filePath):
#     for file in files:
#         if file.endswith(".csv"):
#             rFile = os.path.join(root, file)
#             with open(rFile, 'r') as csvFile:
#                 fileData = csv.reader(csvFile)
#                 next(fileData, None)
#                 # pdb.set_trace()
#                 for data in fileData:
#                     # pdb.set_trace()
#                     allData.append(data)
#             csvFile.close()
# pdb.set_trace()
# # groupData = [list(j) for i, j in groupby(allData, lambda item: pd.to_datetime(item[1]))]
# groupData = [list(j) for i, j in groupby(allData, lambda item: datetime.strptime(item[1], '%d-%m-%Y %H:%M:%S'))]
# # groupData = [list(j) for i, j in groupby(allData, lambda item: datetime.strptime(item[1], '%d%M%Y %H:%M:%S'))]
# for dateData in groupData:
#     pdb.set_trace()
#     dateData.sort(key=lambda x: datetime.strptime(x[1], '%Y%m%d'))
#     minuteData=[x for x in dateData if x[2] > "09:15" and x[2] < "15:31"]

#     arrangedData=[]
#     for data in minuteData:
#         pdb.set_trace()
#         minData=[data[1]+data[2], data[3],
#                    data[4], data[5], data[6], data[7]]
#         arrangedData.append(minData)
#     date=datetime.strptime(dateData[0][1], '%Y%m%d').strftime('%d-%m-%Y')

#     with open('data/structured/nifty_option/minute/' + date + '.json', 'w') as outfile:
#         json.dump(arrangedData, outfile, indent=2)
#     print("File "+date+".json complete")

# print("All Done")
