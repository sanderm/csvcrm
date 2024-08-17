#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys;
import subprocess as sp

global x;
global result1;
global result2;
global result3;

  cmd1= "diff '" + path + "/" | cut -f 2- -d ' ' | tail -n +2 | sort -g | uniq -c | grep -v 'No newline' | egrep -v '\---' | awk '$1 ~ /^1/' | wc -l"
  result1[x] = sp.getoutput(cmd1)

result1=[]
result2=[]
result3=[]
for range(0,xx):
  result1.append("");
  result2.append("");
  result3.append("");
def onefile(file1, x):
  x=1+x;
  print(file1);
  #if "csv$" in file:
  cmd1= "diff '" + path + "/" + file1 + "' test.csv | cut -f 2- -d ' ' | tail -n +2 | sort -g | uniq -c | grep -v 'No newline' | egrep -v '\---' | awk '$1 ~ /^1/' | wc -l"
  result1[x] = sp.getoutput(cmd1)
  debugcmd2= "diff '" + path + "/" + file1 + "' test.csv | cut -f 2- -d ' ' | tail -n +2 | sort -g | uniq -c | grep -v 'No newline' | egrep -v '\---' | awk '$1 ~ /^1/'"
  debug1 = sp.getoutput(debugcmd2)
  cmd2= "diff '" + path + "/" + file1 + "' test.csv | cut -f 2- -d ' ' | tail -n +2 | sort -g | uniq -c | grep -v 'No newline' | egrep -v '\---' | awk '$1 ~ /^2/'"
  result2[x] = sp.getoutput(cmd2)
  cmd3= "cat test.csv | wc -l"
  result3[x] = sp.getoutput(cmd3)
  #result4 = sp.getoutput(cmd4)
  if result1[x] == 0:
    if result2[x]:
      result= str(int(result1[x])/int(result2[x]))
  else:
    result = result1[x]
  print (result1[x], result2[x], result3[x]);
  #result= round(result1 + result2 + result3);
  #print (result)
  return x;

x=0;
path = r'uploads/'
for file1 in os.listdir(path):
  a= onefile(file1, x);
  

def index(req):
  lines_seen = set() # holds lines already seen
  path = r'uploads/'
  patrn = "Coffee"
  for file in os.listdir(path): #added this line
    current_file = os.path.join(path, file)
    for line in open(current_file, "r"):
        if line not in lines_seen: # not a duplicate
          lines_seen.add(line)
          for word in line:
            if re.search(patrn, word):
              print(line);


  return "Hello World! This is a python script!";
