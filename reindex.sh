#grep "Startup Norway" ../../data/ProNorway.csv | sort | awk -F',' '{print $3 "," $12'} 


cat uploads/2020-06-24-172338_Startup\ Norway\ Database.xlsx\ -\ startups\ \(9\).csv.csv | awk -F',' '{print $1}' | while read i; do 
k=(expr $k+1)
egrep "\"$i" ../data/ProNorway.csv | grep -vi "Beate" | sort | awk -F',' '{print $3 "," $8 ", " $12'} | xargs echo -n;
echo
done
