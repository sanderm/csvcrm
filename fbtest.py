import pyrebase
import json

config = {
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "https://tagupexits.firebaseio.com",
  "storageBucket": ""
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# remove all existing elements:
db.remove()

#add new data:
json_data=open("py/jsontest.json").read()
jsontext = json.loads(json_data)
db.set(jsontext)