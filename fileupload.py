#!/usr/bin/env python3

import os
import sys
import datetime
import pyrebase
import json
import csv

file1 = sys.argv[1]

# Check if path exits
if os.path.exists(file1):
    print("File exist")

# Get filename
print ("filename to upload to firebase: " + file1)

# This is the path to the upload directory
uploadfolder = 'uploads/'
# These are the extension that we are accepting to be uploaded
allowedextentions = set(['csv'])

# defines what exstentions is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in allowedextentions

# creates stats about tags and letters on front page i files
def count():
    count = 0
    count2 = 0
    char = ","
    char2 = "\n"
    for filename in os.listdir(uploadfolder):
        if filename.endswith(".csv"):
            fileindir= os.path.join(uploadfolder, filename)
            file = open(fileindir,"r")
            for i in file:
                for c in i:
                    count2= count2 +1
                    if c == char or c == char2:
                        count = count + 1
    file1 = open('tags.txt', 'w')
    file1.write(str(count) + "\n")
    file1.close()
    file1 = open('letters.txt', 'w')
    file1.write(str(count2) + "\n")
    file1.close()

# uploads the filename to files, then filebase
def upload(filename):
    if file1 and allowed_file(filename):
        # Make the filename safe, remove unsupported chars
        #utc_time = datetime.datetime.utcnow()
        #filename = utc_time.strftime("%Y-%m-%d-%H%M%S") + "_" + filename + ".csv"
        savefilename= os.path.join(uploadfolder, filename)

        #file.save(savefilename)
        upload_to_firebase(savefilename)


def upload_to_firebase(filename):
    convert_csv_to_json(filename)

    config = {
        "apiKey": "AIzaSyAKwq2mcUjSxrA-MkCti_s5gLbE4epqDkg",
        "authDomain": "tagupexits2-710aa.firebaseapp.com",
        "databaseURL": "https://tagupexits2-710aa.firebaseio.com",
        "storageBucket": "tagupexits2-710aa.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    
    # remove all existing elements:
    db.remove()
    
    #add new data:
    json_data = open(filename + '.json').read()
    jsontext = json.loads(json_data)
    db.set(jsontext)

def convert_csv_to_json(filename):
    csvfile = open(filename, 'r')
    jsonfile = open(filename + '.json', 'w')
    
    output =[]
    for row in csv.DictReader(csvfile):
        output.append(row)

    json.dump(output,jsonfile,indent=4,sort_keys=False)

if __name__ == "__main__":
  upload(file1)
  count()

