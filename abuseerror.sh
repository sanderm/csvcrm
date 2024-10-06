#!/bin/bash

(echo "textyear, textmonth, textday, texttime, textippid";  tail /var/log/apache2/error.log | awk '{print $5 ", " $2 ", " $3 ", " $4 ", " $10}') | awk -F ']' '{print $1 $2}' |awk -F':' '{print $1 ":" $2", " $3}' | awk '{print $0}' > /root/errorlog.csv; cat /root/errorlog.csv | awk '{print $6'} | xargs -iinsert /root/abuse.sh insert
