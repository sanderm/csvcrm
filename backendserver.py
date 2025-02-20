#!/usr/bin/env python3

# egrep "test" uploads/*csv.csv$* | awk -F':' '{print $2}' | sort | uniq -c | sort -g
import os
import datetime
import pyrebase
import json
import csv
import requests
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_cors import CORS
import venv
#from werkzeug import secure_filename

app = Flask(__name__)
CORS(app)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['csv'])

# creates stats about tags and letters
def count():
    count = 0
    count2 = 0
    char = ","
    char2 = "\n"
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith(".csv"):
            fileindir= os.path.join(app.config['UPLOAD_FOLDER'], filename)
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
    #file1 = open('uploads/all.csv', 'w')
    #file1.write("")
    #file1.close()
    #upload_to_firebase(os.path.join(app.config['UPLOAD_FOLDER'], "all.csv"))
    #print("THE CHARACTER {} IS FOUND {} TIMES IN THE TEXT FILES".format(char,count))
    os.system("/var/www/rockefellerthrust/count.sh");

# defines what exstentions is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask

#def root_dir():  # pragma: no cover
#    return os.path.abspath(os.path.dirname(__file__))


#def get_file(filename):  # pragma: no cover
#    try:
#        src = os.path.join(root_dir(), filename)
#       # Figure out how flask returns static files
#        # Tried:
#        # - render_template
#        # - send_file
#       # This should not be so non-obvious
#       return open(src).read()
#    except IOError as exc:
#        return str(exc)

@app.route('/')
def hello():
    return 'Hello World2'

#@app.route('/', methods=['GET'])
#def metrics():  # pragma: no cover
#    content = get_file('jenkins_analytics.html')
#    return Response(content, mimetype="text/html")

#@app.route('/', defaults={'path': ''})
#@app.route('/<path:path>')
#def get_resource(path):  # pragma: no cover
#    mimetypes = {
 #       ".css": "text/css",
#        ".html": "text/html",

# returns a list of uploaded files
@app.route('/searchform', methods=['GET'])
def searchform():

  lines_seen = set() # holds lines already seen
  path = r'uploads/'
  for file in os.listdir(path): #added this line
    current_file = os.path.join(path, file)
    for line in open(current_file, "r"):
        if line not in lines_seen: # not a duplicate
            print(line);
            lines_seen.add(line)
  subprocess.call(['grep -i startup uploads/*.json | awk -F":        " \'{print $2 " " $1}\' | sort | uniq | wc -l'])
  filename = 'some.csv'
  with open(filename, 'rb') as f:
       reader = csv.reader(f)
       try:
           for row in reader:
               print(row);
       except csv.Error as e:
           sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))


# Route that will process the file upload
@app.route('/search', methods=['GET'])
def search():
    # Get the name of the uploaded file
    match = request.form.get('match')
    f= "uploads/search.csv"
    for line in open(f, 'r'):
        if re.search(search_term, line):
            print (line);
            if line == None:
                print('no matches found')

    cmd= "egrep 'test' uploads/*csv.csv$* | awk -F':' '{print $2}' | sort | uniq -c | sort -g"
    exec(cmd);

@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        utc_time = datetime.datetime.utcnow()
        filename = utc_time.strftime("%Y-%m-%d-%H%M%S") + "_" + file.filename + ".csv"
        # Move the file form the temporal folder to
        # the upload folder we setup
        
        #filediryear= os.path.join(app.config['UPLOAD_FOLDER'], utc_time.strftime("%Y-%m"))
        #os.mkdir(filediryear)
        savefilename= os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # diff test2.csv test.csv | cut -f 2- -d ' ' | tail -n +2 | wc -l

        file.save(savefilename)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        
        upload_to_firebase(savefilename)
        #convert_csv_to_json(savefilename)
        #prettify_csv(savefilename)
        #s = requests.Session()
        #s.headers.update({'referer': my_referer})
        #theurl= s.get(url)
        #theurl= requests.get(url, headers={'referer': my_referer})
        theurl= request.referrer;
        count();
        return redirect(theurl, code=302)

        #return "Success!"

@app.route('/change', methods=['POST'])
def change():
    # Get the name of the uploaded file
    file = request.form.get('changefile')
    # Check if the file is one of the allowed types/extensions
    savefilename= os.path.join(app.config['UPLOAD_FOLDER'], file)
    print ( "$file");
    # Redirect the user to the uploaded_file route, which
    # will basicaly show on the browser the uploaded file
    #print (os.environ.get( ” USERNAME” ));
    upload_to_firebase(savefilename)
    theurl= request.referrer;
    count();
    return redirect(theurl, code=302)

    #return "Success!"

def prettify_csv(csv_file):
    
    #data = csv.reader(csvfile)
    data = []
    toappend= ""
    for row in csv.DictReader(open(csv_file, 'r')):
        #data.append(row)
        toappend += str(row) + "\n"
    
    1. #{
    #    'description': 'Bought by Bayer, First marketed alpha-particle emitting radiopharmaceutics for cancer treatment', 
    #    'url': 'https://en.wikipedia.org/wiki/Algeta', 
    #    'name': 'Algeta', 
    #    'numexityear': '2014', 
    #    'test': 
    # 2.    {
    #        'innerTest': 'Martin'    
    #    }
    #    'curexitM': '2900'
    #},
    #{
    #    'description': 'Bought by Nordic Capital, 3d graphics and maps for the digital broadcast industry. ', 
    #    'url': 'http://www.vizrt.com', 
    #    'name': 'Vizrt', 
    #    'numexityear': '2014', 
    #    'curexitM': '350'
    #}
    
    
    # csv file in a single string
    # 1. "{}" 2. " {
    #
    #              }"
    #        
    
    #print(toappend)

        
    #fd = open(csv_file, 'wb')
    #try:
    #    writer = csv.writer(fd, dialect='excel', quotechar='"', quoting=csv.QUOTE_ALL)
    #    writer.writerows(data)
    
    #finally:
    #    fd.close()


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

# running on https://swapp-sanderm1.c9users.io/ python3 py/mjgtest.py
# html site: https://preview.c9users.io/sanderm1/swapp/tagup/index.html
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
