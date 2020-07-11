#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb;
import sys;
import re;
import simplejson as json
import yaml;
from collections import OrderedDict;

config_str = """
related_companies:
  select_query: 'select replace(c.permalink, " \t", "__") AS permalink,ifnull(group_concat(DISTINCT cc.company_name), "") AS related_company_names,ifnull(group_concat(DISTINCT cc.permalink), "") AS related_permalinks,ifnull(group_concat(DISTINCT cc.logo), "") AS related_logos,ifnull(group_concat(DISTINCT cc.company_description), "") AS related_company_descriptions from company_tag_join5 AS c left join company_tag_join5 AS cc on (c.tags = cc.tags and c.permalink != cc.permalink) group by c.permalink;'

companies:
  select_query: 'select count(t.tag_subcategory) as tag_count, replace(concat(c.company_name, "-", c.company_id)," \t", "__") AS permalink, c.company_id, 
                 orgnr, company_name, website, twitter, founded_date, company_description, logo, facebook, 
                 c.user_id,company_date, 
                 ifnull(group_concat(t.tag_subcategory),"") AS tags, ifnull(group_concat(DISTINCT p.person_name), "") AS person_names, 
                 ifnull(group_concat(DISTINCT p.person_id), "") AS person_ids,ifnull(group_concat(DISTINCT role_name), "") AS role_names, 
                 replace(concat(p.person_name, "-", p.person_id)," ", "_") AS person_permalinks
                 from company as c LEFT OUTER JOIN company_person AS cp 
                 ON (c.company_id = cp.company_id) LEFT JOIN 
                 tag_vertical AS t on (t.tag_vertical_id = c.company_id && t.tag_category = "company") 
                 left outer join person AS p on (cp.person_id = p.person_id) group by company_id order by tag_count DESC;'
  select_query_old2: 'select count(t.tag_subcategory) as tag_count, replace(concat(c.company_name, "-", c.company_id)," ", "_") AS permalink, 
                 c.company_id, \
                 orgnr, c.company_name, website, twitter, founded_date, c.company_description, c.logo, facebook, 
                 c.user_id,company_date, 
                 ifnull(group_concat(t.tag_subcategory),"") AS tags, ifnull(group_concat(DISTINCT p.person_name), "") AS person_names, 
                 ifnull(group_concat(DISTINCT p.person_id), "") AS person_ids,ifnull(group_concat(DISTINCT role_name), "") AS role_names, 
                 ifnull(group_concat(DISTINCT cc.permalink), ""),
                 replace(concat(p.person_name, "-", p.person_id)," ", "_") AS person_permalinks,
                 ifnull(group_concat(DISTINCT cc.company_name), "") AS related_company_names,
                 ifnull(group_concat(DISTINCT cc.permalink), "") AS related_permalinks,
                 ifnull(group_concat(DISTINCT cc.logo), "") AS related_logos,
                 ifnull(group_concat(DISTINCT cc.company_description), "") AS related_company_descriptions
                 from company as c LEFT OUTER JOIN company_person AS cp 
                 ON (c.company_id = cp.company_id) LEFT JOIN 
                 tag_vertical AS t on (t.tag_vertical_id = c.company_id && t.tag_category = "company") 
                 left outer join person AS p on (cp.person_id = p.person_id) 
                 left join company_tag_join5 AS ccc on (ccc.permalink = permalink)
                 left join company_tag_join5 AS cc on (ccc.tags = cc.tags and ccc.permalink != cc.permalink)
                 group by company_id order by tag_count DESC;'

  select_query2: 'select c.id, c.orgnr,c.name, group_concat(t.name) AS tags,count(t.name) as tag_num,c.homepage_url,
                 c.category,c.twitter_username,c.founded_year,description,c.logo,c.city,c.industry,
                 c.facebook,c.lat,c.lng,c.permalink,c.type from base_company AS c 
                 LEFT JOIN taggit_taggeditem AS tt on (c.id = tt.tag_id) 
                 LEFT JOIN taggit_tag AS t ON (tt.object_id = t.id)
                 where c.approved = 1 group by c.name ORDER BY tag_num DESC'
  select_query_old: 'select company_name,group_concat(tag_name),website,twitter from company AS c left join company_tag as t on t.company_id = c.company_id WHERE company_tag_status = "C" and company_status = "C"'
  update_query: "update from"
  insert_query: "insert into"
persons: 
  select_query2: 'select p.person_id,person_name,email,birthyear, location, nationality, ifnull(group_concat(company_name), "") AS company_names, ifnull(group_concat(c.company_description), "") AS company_descriptions, ifnull(group_concat(c.logo), "") AS logos from person as p LEFT JOIN company_person AS cp ON (p.person_id = cp.person_id) LEFT JOIN company AS c ON (cp.company_id = c.company_id) group by person_id;'
  select_query: 'select count(t.tag_subcategory) as tag_count, replace(concat(p.person_name, "-", p.person_id)," \t", "__") AS permalink, 
                 p.person_id,person_name,email,birthyear, location, nationality, ifnull(group_concat(DISTINCT t.tag_subcategory),"") AS skills, 
                 ifnull(group_concat(DISTINCT c.company_name), "") AS company_names, 
                 ifnull(group_concat(DISTINCT c.company_description), "") AS company_descriptions, 
                 ifnull(group_concat(DISTINCT c.logo), "") AS logos,
                 ifnull(group_concat(DISTINCT(concat(c.company_name, "-", c.company_id))), "") AS company_permalinks
                 from person as p
                 left join tag_vertical AS t on (t.tag_vertical_id = p.person_id && t.tag_category ="person") 
                 LEFT JOIN company_person AS cp ON (p.person_id = cp.person_id)
                 LEFT JOIN company AS c ON (cp.company_id = c.company_id) group by person_id order by tag_count DESC;'
tags:
  select_query: 'select tag_subcategory,count(*) AS tag_count from tag_vertical group by tag_subcategory order by tag_count DESC;'
""";
config= yaml.load(config_str);

def FetchOneAssoc(cursor) :
    data = cursor.fetchone()
    if data == None :
        return None
    desc = cursor.description

    dict = OrderedDict();

    for (name, value) in zip(desc, data) :
        dict[name[0]] = value

    return dict

def json_escape(thestring):
  thestring= str(thestring).strip();
  thestring= re.sub(r'([\" \'])', r'\\\1', thestring)
  return thestring;

def make_json():
  json= "";
  con = mdb.connect('localhost', 'frode_nobase', 'startup123', 'frode_nobase')
  with con: 
    cur = con.cursor();
    #json +="var globalData = { ";
    json +="{ ";
    k=0;
    for menu_entry in [ "persons", "companies", "tags", "related_companies"]:
    #for menu_entry in [ "persons"]:
      if k!= 0:
        json+= ",\n";
      k= k+1;
      sql= config[menu_entry]['select_query'];
      #print sql;
      cur.execute(sql);
      json += "\"" + menu_entry +"\": {";
      #json += "\"" + menu_entry +"\": [{";
      #json += " { \"companies\": [{";
      i=0;
      while True:
        sqlresult= FetchOneAssoc(cur);
        j=0;
        if sqlresult == None:
          break;
        else:
          if i!=0:
            if i!=1:
              json += ",\n";
              #json += "} ,\n {";
            #json += "} ";
            json += jsondictstart + jsonadd + " } ";
            #print jsondictstart + jsonadd;
          jsonadd= "";
          for sqlkey, sqlvalue in sqlresult.iteritems():
	    if j!=0:
              jsonadd += ",\n";
            if sqlkey.endswith("s"):
              sqlvalues= re.split(",",json_escape(sqlvalue));
              jsonadd+= "\"" + sqlkey + "\": [";
              k=0;
              for sqlvaluesentry in sqlvalues:
                if k != 0:
                  jsonadd+= ",";
                if sqlvaluesentry != "":
                  jsonadd+= '"' + sqlvaluesentry + '"';
                k=k+1;
              jsonadd+= "]";
            else:
              jsonadd+= "\"" + sqlkey+ "\": \"" + json_escape(sqlvalue) + '"';
            if sqlkey == "permalink":
              jsondictstart= "\"" + json_escape(sqlvalue) + "\": { \n";
              #print jsondictstart;
            j= j+1;
        i= i+1;
      #json += "}]\n";
      json += "}\n";
    json += "}";
  return json;

def make_json2():
  json= "";
  con = mdb.connect('localhost', 'frode_nobase', 'startup123', 'frode_nobase')
  with con: 
    cur = con.cursor();
    #cur.execute("select c.id, c.name, group_concat(t.name) AS tag,count(t.name) as tags,c.homepage_url,c.category,c.twitter_username,c.founded_year,description,c.logo,c.city,c.industry,c.facebook,c.lat,c.lng,c.permalink from base_company AS c LEFT JOIN taggit_taggeditem AS tt on (c.id = tt.tag_id) LEFT JOIN taggit_tag AS t ON (tt.object_id = t.id) where c.approved = 1 group by c.name ORDER BY tags DESC limit 20;");

    cur.execute("select c.id, c.name, group_concat(t.name) AS tag,count(t.name) as tags,c.homepage_url,c.category,c.twitter_username,c.founded_year,description,c.logo,c.city,c.industry,c.facebook,c.lat,c.lng,c.permalink,c.type from base_company AS c LEFT JOIN taggit_taggeditem AS tt on (c.id = tt.tag_id) LEFT JOIN taggit_tag AS t ON (tt.object_id = t.id) where c.approved = 1 group by c.name ORDER BY tags DESC");

    rows = cur.fetchall();

    json += "var globalData = { \"companies\": [";
#id  | name | tag | tags | homepage_url | category | twitter_username | founded_year | description
# | logo                                | city        | industry | facebook |

    i=0;
    for row in rows:
      if i != 0:
        json+= ",";
      json+= "{ \"id\": \"" + json_escape(row[0]) + '", ';
      json+= "\"name\": \"" + json_escape(row[1]) + '", ';
      tags= re.split(",",json_escape(row[2]));
      json+= "\"tags\": [";
      j=0;
      for tag in tags:
        if j != 0:
          json+= ",";
        json+= '"' + tag + '"';
        j=j+1;
      json+= "],";
      json+= "\"homepage_url\": \"" + json_escape(row[4]) + '", ';
      json+= "\"category\": \"" + json_escape(row[5]) + '", ';
      json+= "\"twitter_username\": \"" + json_escape(row[6]) + '", ';
      json+= "\"founded_year\": \"" + json_escape(row[7]) + '", ';

      json+= "\"description\": \"" + json_escape(row[8]) + '", ';
      json+= "\"logo\": \"" + json_escape(row[9]) + '", ';
      json+= "\"city\": \"" + json_escape(row[10]) + '", ';
      json+= "\"industry\": \"" + json_escape(row[11]) + '", ';
      json+= "\"facebook\": \"" + json_escape(row[12]) + '", ';
      json+= "\"lat\": \"" + json_escape(row[13]) + '", ';
      json+= "\"lng\": \"" + json_escape(row[14]) + '", ';
      json+= "\"permalink\": \"" + json_escape(row[15]) + '", ';
      json+= "\"type\": \"" + json_escape(row[16]) + '"';
      json+= "}"
      i= i+1;
    json+= "]}";
    return json;
#		name: "",
#		homepage_url: "",
#		category: "",
#		logo: "",
#		tags: [	"ikt", "cool stuff", "test"]
 #             }, {
#	}]

#}

print make_json();
#data = json.load(make_json());
#print json.dumps(data, separators=(',',':'))
def index(req):
    return "Hello World! This is a python script!";
