cat ip2nation.sql | awk -F"'" '{print $2 ", " $8 "" $11}'  | awk -F ")" '{print $1}' > uploads/ip2nation.csv
cat sms.js | awk -F"'" '{print $2 ", " $6 ", " $10}' > uploads/sms.csv
