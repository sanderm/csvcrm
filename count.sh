# copy to /etc/cron.hourly/ change www dir:
cd /var/www/rockefellerthrust/
(zcat /var/log/apache2/access.log.*.gz; cat /var/log/apache2/access.log.1 /var/log/apache2/access.log)| awk '{print $7 "," $4 "," $1 "," $12}'| sort |egrep "^/" | grep jquery | wc -l > uniq.txt
(zcat /var/log/apache2/access.log.*.gz; cat /var/log/apache2/access.log.1 /var/log/apache2/access.log)| awk '{print $7 "," $4 "," $1 "," $12}'| sort |egrep "^/" | wc -l > pages.txt
echo "textpage, textdate, textip, textbrowserversion" > uploads/uniq.csv; (zcat /var/log/apache2/access.log.*.gz; cat /var/log/apache2/access.log.1 /var/log/apache2/access.log)| awk '{print $7 "," $4 "," $1 "," $12}'| sort |egrep "^/" | grep jquery >> uploads/uniq.csv
echo "textpage, textdate, textip, textbrowserversion" > uploads/pages.csv; (zcat /var/log/apache2/access.log.*.gz; cat /var/log/apache2/access.log.1 /var/log/apache2/access.log)| awk '{print $7 "," $4 "," $1 "," $12}'| sort |egrep "^/" >> uploads/pages.csv
