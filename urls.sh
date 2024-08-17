grep "http://" uploads/*.csv | awk -F'http://' '{print $2}' | awk -F',' '{print $1}' | sort -g | uniq -c | sort -g
