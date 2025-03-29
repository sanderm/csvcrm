# copy to /etc/cron.hourly/ change www dir:
cd /var/www/rockefellerthrust/
(zcat /var/log/apache2/access.log.*.gz; cat /var/log/apache2/access.log.1 /var/log/apache2/access.log)| awk '{print $7 "," $4 "," $1 "," $12}'| sort |egrep "^/" | grep jquery | wc -l > uniq.txt
(zcat /var/log/apache2/access.log.*.gz; cat /var/log/apache2/access.log.1 /var/log/apache2/access.log)| awk '{print $7 "," $4 "," $1 "," $12}'| sort |egrep "^/" | wc -l > pages.txt
echo "textpage, textdate, textip, textbrowserversion" > uploads/uniq.csv; (zcat /var/log/apache2/access.log.*.gz; cat /var/log/apache2/access.log.1 /var/log/apache2/access.log)| awk '{print $7 "," $4 "," $1 "," $12}'| sort |egrep "^/" | grep jquery >> uploads/uniq.csv
echo "textpage, textdate, textip, textbrowserversion" > uploads/pages.csv; (zcat /var/log/apache2/access.log.*.gz; cat /var/log/apache2/access.log.1 /var/log/apache2/access.log)| awk '{print $7 "," $4 "," $1 "," $12}'| sort |egrep "^/" >> uploads/pages.csv
treedays="$(cat /var/log/apache2/access.log /var/log/apache2/access.log.1 | awk '{print  $7 "," $4 "," $1 "," $2}' | sort | awk -F/ '{print     }'| egrep '12|15|23' | wc -l)"
echo "$(((($treedays / 3 ) / 24 ) / 60))" > pagesminutes.txt
uniqdays="$(cat /var/log/apache2/access.log /var/log/apache2/access.log.1 | awk '{print  $7 "," $4 "," $1 "," $12}' | sort | awk -F/ '{print     }'| egrep '12|15|23' | uniq | wc -l)"
echo "$(((($uniqdays / 3 ) / 24 ) / 60))" > uniqminutes.txt
cat /var/log/apache2/access.log /var/log/apache2/access.log.1 | awk '{print $1 "," $12}' | uniq | sort -g | uniq -c | sort -g> uploads/uniq-ip.csv
cat /var/log/apache2/access.log /var/log/apache2/access.log.1 | awk '{print $1 "," $12}' | uniq | sort -g > uploads/uniq-ip-first.csv
zcat /var/log/apache2/access.log.*.gz | awk '{print $1 "," $12}' | uniq | sort -g  > uploads/uniq-ip-last.csv
