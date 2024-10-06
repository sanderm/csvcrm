import os
import csv
import pandas as pd

pathName = os.getcwd()

numFiles = []
# every file in a directory
fileNames = os.listdir(pathName)
for fileNames in fileNames:
    if fileNames.endswith(".csv"):
        numFiles.append(fileNames)

# every csv file in a directory
for i in numFiles:
    file = open(os.path.join(pathName, i))
    #df = pd.read_csv(file)
    reader = list(csv.DictReader(file, delimiter=','))
    #print(reader)
    for k in reader:
        print(k)
        #if v.startswith('url'):
           #print(v)
    #for x in df.keys().startwith('url'):
       #new_df = df.loc[df.startswith['url'] == x]
       # you can use list of file path for saving results   
       #new_df.to_csv('results.csv')
       
    #for type in k:
    #   print(', '.join(type))
    #print("\n");
    #for column in reader:
     #   print(column[4])
